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


def _teaserlist_cachekey(method, context, data):
    return (data.id,
            time() // (60 * CACHETIME))

#@ram.cache(_teaserlist_cachekey)
def _teaserlist(context, data):
    context = aq_inner(context)
    cat = getToolByName(context,'portal_catalog')
    query = {}
    query['Type'] = 'Teaser'
    # show only selected importances
    query['importance'] = data.importance_levels
    # show only published and not expired, even for admins
    query['review_state'] = 'published'
    query['effectiveRange'] = DateTime()
    brains = cat(**query)
    # make a weighted (multiplied by importance) list of teasers.
    teasers = []
    [teasers.extend(int(brain.importance) * [brain]) for brain in brains]
    return teasers

def get_teasers(context, data, request):
    teasers = _teaserlist(context, data)
    if not teasers: return None

    # get used id's from request and exclude em
    taken_teasers = getattr(request, 'teasers', [])

    choosen_teasers = []
    for cnt in range(data.num_teasers):

        # reduce selected teasers with all taken_teasers
        teasers = [teaser for teaser in teasers
                  if teaser.id not in taken_teasers]
        if not teasers: break

        # randomly select num_teasers from all
        choosen_teaser = random.choice(teasers)
        choosen_teasers.append(choosen_teaser.getObject())
        taken_teasers.append(choosen_teaser.id)

    # save new taken teaser list in request
    request['teasers'] = taken_teasers

    # create data structure and return
    scale = data.image_size
    show_title = data.show_title
    show_desc = data.show_description
    altimg = data.prefer_altimage
    return [{'title': show_title and teaser.title or None,
             'image': altimg and getattr(teaser, 'altimage', False) and\
                      teaser.getField('altimage').tag(teaser, scale=scale,\
                          alt=teaser.title, title=teaser.title) or\
                      getattr(teaser, 'image', False) and\
                      teaser.getField('image').tag(teaser, scale=scale,\
                          alt=teaser.title, title=teaser.title) or\
                      None,
             'description': show_desc and teaser.Description() or None,
             'url': teaser.getLink_internal() and\
                    teaser.getLink_internal().absolute_url() or\
                    teaser.link_external or None}
            for teaser in choosen_teasers]


class ITeaserPortlet(IPortletDataProvider):

    importance_levels = schema.Tuple(
            title=_(u'portlet_label_importance_levels', default=u'Importance Levels'),
            description=_(u'portlet_help_importance_levels', default=u'Select which importance levels the portlet should show.'),
            default=(DEFAULT_IMPORTANCE,),
            required=True,
            value_type=schema.Choice(
                vocabulary="collective.teaser.ImportanceVocabulary"
                )
            )

    image_size = schema.Choice(
            title=_(u'portlet_label_image_size', default=u'Image Size'),
            description=_(u'portlet_help_image_size', default=u'Select, which image scale should be used for the portlet.'),
            required=True,
            default=None,
            vocabulary="collective.teaser.ImageScaleVocabulary")

    prefer_altimage = schema.Bool(
        title=_(u'portlet_label_altimage', default=u'Prefer alternative image'),
        description=_(u'portlet_help_altimage', default=u'If an alternative image is defined for the teaser, '\
                u'use this one. Alternative images can have a different layout, '\
                u'e.g. portrait instead of landscape.'),
        default=False)

    show_title = schema.Bool(
        title=_(u'portlet_label_show_title', default=u'Show title'),
        description=_(u'portlet_help_show_title', default=u'Show the title of the teaser.'),
        default=True)

    show_description = schema.Bool(
        title=_(u'portlet_label_show_description', default=u'Show description'),
        description=_(u'portlet_help_show_description', default=u'Show the description of the teaser as text below the image.'),
        default=True)

    num_teasers = schema.Int(
        title=_(u'portlet_label_num_teasers', default=u'Number of teasers'),
        description=_(u'portlet_help_num_teasers', default=u'Define the maximum number of teasers, '\
                u'which are displayed in this portlet'),
        default=1)


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('teaser_portlet.pt')

    @property
    def teasers(self):
        return get_teasers(self.context, self.data, self.request)

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

    show_description = False

    def __init__(self, importance_levels=None,
            image_size=None,
            prefer_altimage=False,
            show_title=True,
            show_description=False,
            num_teasers=1):
        self.importance_levels = importance_levels
        self.image_size = image_size
        self.prefer_altimage = prefer_altimage
        self.show_title=show_title
        self.show_description=show_description
        self.num_teasers=num_teasers

    @property
    def title(self):
        return _(u'portlet_teaser_title', default=u"Teaser")


class AddForm(base.AddForm):
    form_fields = form.Fields(ITeaserPortlet)
    label = _(u'portlet_label_add', default=u"Add portlet to show teasers.")
    description = _(u'portlet_help_add', default=u"This portlet shows teasers.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ITeaserPortlet)
    label = _(u'portlet_label_add', default=u"Add portlet to show teasers.")
    description = _(u'portlet_help_add', default=u"This portlet shows teasers.")
