# -*- coding: utf-8 -*-
import random
from time import time
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.formlib import form
from zope.interface import implements, implementer
from zope import schema
from plone.memoize import ram
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner, aq_base
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.teaser.interfaces import IPortletAvailable
from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser import MsgFact as _

CACHETIME = 30 # time to cache catalog query in minutes


@implementer(IPortletAvailable)
def teaser_default_available(portlet, manager, context):
    return True


def _teaserlist_cachekey(method, self):
    return (self.data.id,
            time() // (60 * CACHETIME))


class ITeaserPortlet(IPortletDataProvider):

    importance_levels = schema.Tuple(
            title=_(u'Importance Levels'),
            description=_(u'Select which importance levels the portlet should show.'),
            default=(DEFAULT_IMPORTANCE,),
            required=True,
            value_type=schema.Choice(
                vocabulary="collective.teaser.ImportanceVocabulary"
                )
            )

    image_size = schema.Choice(
            title=_(u'Image Size'),
            description=_(u'Select, which image scale should be used for the portlet.'),
            required=True,
            default=None,
            vocabulary="collective.teaser.ImageScaleVocabulary")

    prefer_altimage = schema.Bool(
        title=_(u'Prefer alternative image'),
        description=_(u'If an alternative image is defined for the teaser,'\
                u'use this one. Alternative images can have a different layout,'\
                u'e.g. portrait instead of landscape.'),
        default=False)

    show_title = schema.Bool(
        title=_(u'Show the teasers title'),
        description=_(u'Show the title of the teaser which is displayed.'\
                u'Note, that text defined in the teaser is always displayed,'\
                u'if defined'),
        default=True)

    num_teasers = schema.Int(
        title=_(u'Number of teasers displayed'),
        description=_(u'Define the maximum number of teasers,'\
                u'which are displayed in this portlet'),
        default=1)


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('teaser_portlet.pt')

    @ram.cache(_teaserlist_cachekey)
    def _teaserlist(self):
        context = aq_inner(self.context)
        cat = getToolByName(context,'portal_catalog')
        query = {}
        query['Type'] = 'Teaser'
        # show only selected importances
        query['importance'] = self.data.importance_levels
        # show only published and not expired, even for admins
        query['review_state'] = 'published'
        query['effectiveRange'] = DateTime()
        brains = cat(**query)
        # make a weighted (multiplied by importance) list of teasers.
        teasers = []
        [teasers.extend(int(brain.importance) * [brain]) for brain in brains]
        return teasers

    def get_teasers(self):
        teasers = self._teaserlist()
        if not teasers: return None

        # get used id's from request and exclude em
        taken_teasers = getattr(self.request, 'teasers', [])

        choosen_teasers = []
        for cnt in range(self.data.num_teasers):

            # reduce selected teasers with all taken_teasers
            teasers = [teaser for teaser in teasers
                      if teaser.id not in taken_teasers]
            if not teasers: break

            # randomly select num_teasers from all
            choosen_teaser = random.choice(teasers)
            choosen_teasers.append(choosen_teaser.getObject())
            taken_teasers.append(choosen_teaser.id)

        # save new taken teaser list in request
        self.request['teasers'] = taken_teasers

        # create data structure and return
        scale = self.data.image_size
        title = self.data.show_title
        altimg = self.data.prefer_altimage
        # below: give "tag" the title and alt attr as unicode objects
        # P.Archetypes.Field.ImageField.tag otherwise will throw an error
        return [{'title': title and u'%s' % teaser.title or u'',
                 'image': altimg and getattr(teaser, 'altimage', False) and\
                          teaser.getField('altimage').tag(teaser, scale=scale,\
                              alt=teaser.title, title=teaser.title) or\
                          getattr(teaser, 'image', False) and\
                          teaser.getField('image').tag(teaser, scale=scale,\
                              alt=teaser.title, title=teaser.title) or\
                          None,
                 'text': teaser.text,
                 'url': teaser.getLink_internal() and\
                        teaser.getLink_internal().absolute_url() or\
                        teaser.link_external or None}
                for teaser in choosen_teasers]

    @property
    def available(self):
        context = aq_inner(self.context)
        assignment = aq_base(self.data)
        # first try to get a named multi adapter, then an unnamed
        available = queryMultiAdapter(
            (assignment, self.manager, context), IPortletAvailable, name=assignment.id,
            default=getMultiAdapter((assignment, self.manager, context), IPortletAvailable))
        return available


class Assignment(base.Assignment):
    implements(ITeaserPortlet)

    def __init__(self, importance_levels=None,
            image_size=None,
            prefer_altimage=False,
            show_title=True,
            num_teasers=1):
        self.importance_levels = importance_levels
        self.image_size = image_size
        self.prefer_altimage = prefer_altimage
        self.show_title=show_title
        self.num_teasers=num_teasers

    @property
    def title(self):
        return _(u"Teaser")


class AddForm(base.AddForm):
    form_fields = form.Fields(ITeaserPortlet)
    label = _(u"Add portlet to show teasers.")
    description = _(u"This portlet shows teasers.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ITeaserPortlet)
    label = _(u"Add portlet to show teasers.")
    description = _(u"This portlet shows teasers.")


