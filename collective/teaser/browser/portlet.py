# -*- coding: utf-8 -*-
import uuid
from zope.component import (
    getUtility,
    getMultiAdapter,
    queryMultiAdapter,
)
from zope.formlib import form
from zope.interface import implements, implementer
from zope import schema
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import (
    IPortletManager,
    IPortletAssignmentMapping,
)
from Acquisition import (
    aq_inner,
    aq_base,
    aq_parent,
)
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.teaser.interfaces import IPortletAvailable
from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser import MsgFact as _
from collective.teaser.browser.common import get_teasers


@implementer(IPortletAvailable)
def teaser_default_available(portlet, manager, context):
    return True


def get_portlet_assingment(context, uid):
    for name in [u"plone.leftcolumn", u"plone.rightcolumn",
                 u"collective.teaser.portletmanager"]:
        manager = getUtility(IPortletManager, name=name)
        for category in manager.values():
            for group in category.values():
                for assignment in group.values():
                    if ITeaserPortlet.providedBy(assignment):
                        if uid == assignment.uid:
                            return assignment
        context = aq_inner(context)
        while True:
            try:
                assignment_mapping = getMultiAdapter((context, manager),
                                                     IPortletAssignmentMapping)
            except:
                return
            for assignment in assignment_mapping.values():
                if ITeaserPortlet.providedBy(assignment):
                    if uid == assignment.uid:
                        return assignment
            if IPloneSiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(context))


class ITeaserPortlet(IPortletDataProvider):

    importance_levels = schema.Tuple(
        title=_(u'portlet_label_importance_levels',
                default=u'Importance Levels'),
        description=_(u'portlet_help_importance_levels',
                      default=u'Select which importance levels the portlet ' +\
                              u'should show.'),
        default=(DEFAULT_IMPORTANCE,),
        required=True,
        value_type=schema.Choice(
            vocabulary="collective.teaser.ImportanceVocabulary"),
        )

    teaser_scale = schema.Choice(
        title=_(u'portlet_label_image_scale', default=u'Image Scale'),
        description=_(u'portlet_help_image_scale',
                      default=u'Select, which image scale should be used ' +\
                              u'for the portlet.'),
        required=True,
        default=None,
        vocabulary="collective.teaser.ImageScaleVocabulary",
        )

    show_title = schema.Bool(
        title=_(u'portlet_label_show_title', default=u'Show title'),
        description=_(u'portlet_help_show_title',
                      default=u'Show the title of the teaser.'),
        default=True,
        )

    show_description = schema.Bool(
        title=_(u'portlet_label_show_description', default=u'Show description'),
        description=_(u'portlet_help_show_description',
                      default=u'Show the description of the teaser as text ' +\
                              u'below the image.'),
        default=True,
        )

    num_teasers = schema.Int(
        title=_(u'portlet_label_num_teasers', default=u'Number of teasers'),
        description=_(u'portlet_help_num_teasers',
                      default=u'Define the maximum number of teasers, which ' +\
                              u'are displayed in this portlet'),
        default=1,
        )


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
            (assignment, self.manager, context),
            IPortletAvailable,
            name=assignment.id,
            default=getMultiAdapter((assignment, self.manager, context),
                                    IPortletAvailable))
        return available


class Assignment(base.Assignment):
    implements(ITeaserPortlet)

    show_description = False

    def __init__(self, importance_levels=None,
            teaser_scale=None,
            show_title=True,
            show_description=False,
            num_teasers=1):
        self.uid = uuid.uuid4()
        self.importance_levels = importance_levels
        self.teaser_scale = teaser_scale
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