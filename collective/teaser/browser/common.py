import random
from zope import schema
from zope.formlib import form
from zope.interface import implements
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize import ram
from time import time

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser import MsgFact as _

CACHETIME = 30 # time to cache catalog query in minutes

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
                'use this one. Alternative images can have a different layout,'\
                'e.g. portrait instead of landscape.'),
        default=False)

    show_title = schema.Bool(
        title=_(u'Show the teasers title'),
        description=_(u'Show the title of the teaser which is displayed.'\
                'Note, that text defined in the teaser is always displayed,'\
                'if defined'),
        default=True)

    num_teasers = schema.Int(
        title=_(u'Number of teasers displayed'),
        description=_(u'Define the maximum number of teasers,'\
                'which are displayed in this portlet'),
        default=1)


def _teaserlist_cachekey(method, self):
    return (self.__portlet_metadata__['name'],
            time() // (60 * CACHETIME))


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
        return [{'title': title and teaser.title or None,
                 'image': altimg and getattr(teaser, 'altimage', False) and\
                          teaser.getField('altimage').tag(teaser, scale=scale) or\
                          getattr(teaser, 'image', False) and\
                          teaser.getField('image').tag(teaser, scale=scale) or\
                          None,
                 'text': teaser.text,
                 'url': teaser.getLink_internal() and\
                        teaser.getLink_internal().absolute_url() or\
                        teaser.link_external or None}
                for teaser in choosen_teasers]

    @property
    def available(self):
        return True


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
        return _(u"Teaser Portlet")


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


