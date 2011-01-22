from zope import schema
from zope.formlib import form
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser import MsgFact as _

class ITeaserPortlet(IPortletDataProvider):
    importance_levels = schema.List(
            title=_(u'Importance Levels'),
            description=_(u'Select which importance levels the portlet should show.'),
            default=DEFAULT_IMPORTANCE,
            required=True,
            value_type=schema.Choice(
                vocabulary="collective.teaser.ImportanceVocabulary"
                )
            )
    image_size = schema.List(
            title=_(u'Image Size'),
            description=_(u'Select, which image scale should be used for the portlet.'),
            required=True,
            default=None,
            value_type=schema.Choice(
                vocabulary="collective.teaser.ImageScaleVocabulary"
                )
            )
    prefer_altimage = schema.Bool(
        title=_(u'Prefer alternative image'),
        description=_(u'If an alternative image is defined for the teaser,'\
                'use this one. Alternative images can have a different layout,'\
                'e.g. portrait instead of landscape.'),
        default=False)


class Assignment(base.Assignment):
    implements(ITeaserPortlet)

    def __init__(self, importance_levels=None,
            image_size=None,
            prefer_altimage=False):
        self.importance_levels = importance_levels
        self.image_size = image_size
        self.prefer_altimage = prefer_altimage

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

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('teaser_portlet.pt')

    @property
    def available(self):
        return True


