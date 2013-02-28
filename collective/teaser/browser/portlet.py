# -*- coding: utf-8 -*-
import uuid
from node.utils import instance_property
from zope.component import (
    getUtility,
    getMultiAdapter
)
from zope.interface import implements
from zope import schema
from zope.schema.vocabulary import (
    SimpleVocabulary,
    SimpleTerm,
)
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from plone.memoize.view import memoize
#from plone.memoize import ram
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import get_language
from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import (
    IPortletManager,
    IPortletAssignmentMapping,
)
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from Acquisition import (
    aq_inner,
    aq_parent,
)
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser.browser.common import get_teasers

_ = MessageFactory('collective.teaser')


def render_cachekey(fun, self):
    """
    Based on render_cachekey from plone.app.portlets.cache, without the
    fingerprint based on the portlet's catalog brains.

    Generates a key based on:

    * Portal URL
    * Negotiated language
    * Anonymous user flag
    * Portlet manager
    * Assignment

    """
    context = aq_inner(self.context)
    anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()

    return "".join((
        getToolByName(aq_inner(self.context), 'portal_url')(),
        get_language(aq_inner(self.context), self.request),
        str(anonymous),
        self.manager.__name__,
        self.data.__name__))


def get_portlet_assingment(context, uid):
    context_orgin = context
    for name in [u"plone.leftcolumn", u"plone.rightcolumn",
                 u"collective.teaser.portletmanager"]:
        manager = getUtility(IPortletManager, name=name)
        for category in manager.values():
            for group in category.values():
                for assignment in group.values():
                    if ITeaserPortlet.providedBy(assignment):
                        if uid == str(assignment.uid):
                            return assignment
        context = aq_inner(context_orgin)
        while True:
            try:
                assignment_mapping = getMultiAdapter((context, manager),
                                                     IPortletAssignmentMapping)
            except:
                return
            for assignment in assignment_mapping.values():
                if ITeaserPortlet.providedBy(assignment):
                    if uid == str(assignment.uid):
                        return assignment
            if IPloneSiteRoot.providedBy(context):
                break
            context = aq_parent(aq_inner(context))
    raise KeyError(u"Portlet assignment for uid '%s' not found." % uid)


class TeaserRenderer(object):
    template = PageTemplateFile('teaser.pt')

    def __init__(self, context, data, request):
        self.context = context
        self.data = data
        self.request = request

    def __call__(self):
        return self.template(options=self)

    @property
    def display_columns(self):
        return int(self.data.display_columns)

    @property
    def table_rows(self):
        count = len(self.teasers)
        if count == 1:
            return count
        rows = count / 2
        if count % 2 != 0:
            rows += 1
        return rows

    @instance_property
    def teasers(self):
        return get_teasers(self.context, self.data, self.request)


class AjaxTeaser(BrowserView):

    def __call__(self):
        return TeaserRenderer(self.context, self.data, self.request)()

    @property
    def data(self):
        return get_portlet_assingment(self.context, self.request.get('uid'))


display_columns = SimpleVocabulary([
    SimpleTerm(value=u'1', title=_(u'One')),
    SimpleTerm(value=u'2', title=_(u'Two'))])


class ITeaserPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=False)

    display_columns = schema.Choice(
        title=_(u'portlet_label_display_columns', default=u'Number of columns'),
        description=_(u'portlet_help_display_columns',
                      default=u'Select number of columns to display'),
        vocabulary=display_columns,
        default=u'1',
        required=True,
        )

    importance_levels = schema.Tuple(
        title=_(u'portlet_label_importance_levels',
                default=u'Importance Levels'),
        description=_(u'portlet_help_importance_levels',
                      default=u'Select which importance levels the portlet '
                              u'should show.'),
        default=(DEFAULT_IMPORTANCE,),
        required=True,
        value_type=schema.Choice(
            vocabulary="collective.teaser.ImportanceVocabulary"),
        )

    keywords_filter = schema.Tuple(
        title=_(u'portlet_label_keywords_filter',
                default=u'Keywords Filter'),
        description=_(u'portlet_help_keywords_filter',
                      default=u'Select which teasers with specific keywords '
                              u'should be shown. Select none to order to show '
                              u'any teasers.'),
        default=None,
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.Keywords"),
        )

    teaser_scale = schema.Choice(
        title=_(u'portlet_label_image_scale', default=u'Image Scale'),
        description=_(u'portlet_help_image_scale',
                      default=u'Select, which image scale should be used '
                              u'for the portlet.'),
        required=True,
        default=None,
        vocabulary="collective.teaser.ImageScaleVocabulary",
        )

    num_teasers = schema.Int(
        title=_(u'portlet_label_num_teasers', default=u'Number of teasers'),
        description=_(u'portlet_help_num_teasers',
                      default=u'Define the maximum number of teasers, which '
                              u'are displayed in this portlet'),
        default=1,
        required=True,
        )

    ajaxified = schema.Bool(
        title=_(u'portlet_label_ajaxified', default=u'Load Teasers via AJAX?'),
        description=_(u'portlet_help_ajaxified',
                      default=u'Whether teaser is loaded deferred via ajax '
                              u'or directly.'),
        default=True,
        required=False,
        )


    show_title = schema.Bool(
        title=_(u'portlet_label_show_title', default=u'Show title'),
        description=_(u'portlet_help_show_title',
                      default=u'Show the title of the teaser.'),
        default=True,
        required=False,
        )

    show_description = schema.Bool(
        title=_(u'portlet_label_show_description', default=u'Show description'),
        description=_(u'portlet_help_show_description',
                      default=u'Show the description of the teaser as text ' +\
                              u'below the image.'),
        default=False,
        required=False,
        )

    search_base = schema.Choice(
        title=_(u'portlet_label_search_base', default=u'Search base'),
        description=_(u'portlet_help_search_base',
                      default=u'Select teaser search base folder'),
        source=SearchableTextSourceBinder({'is_folderish': True},
                                           default_query='path:'),
        required=False,
        )


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('teaser_portlet.pt')

    # On default pages, portlets are called twice (parent and default page).
    # When the teaser is going to be displayed on a default page, the teaser is
    # called twice. This seems to be a bug/default-page-sideeffect in Plone.
    # When only one teaser is available for that portlet, on the second call
    # it's removed from the available teasers, since it's already in the
    # taken_teasers list. As a result, no teaser is shown. Therefore, we cache
    # the render call.
    #@ram.cache(render_cachekey) # cached per request
    @memoize
    def renderer(self):
        return TeaserRenderer(self.context, self.data, self.request)

    @property
    def display(self):
        return bool(self.renderer().teasers)

    @property
    def rendered_teasers(self):
        return self.renderer()

    def has_header(self):
        return bool(self.data.header)


class Assignment(base.Assignment):
    implements(ITeaserPortlet)

    # avoid upgrade pain
    show_description = False
    keywords_filter = None
    search_base = None

    def __init__(self, importance_levels=None,
            keywords_filter=None,
            teaser_scale=None,
            num_teasers=1,
            ajaxified=True,
            show_title=True,
            show_description=False,
            search_base=None,
            header=u'',
            display_columns=u'1'):
        self._header = header
        self._display_columns = display_columns
        self.importance_levels = importance_levels
        self.keywords_filter = keywords_filter
        self.teaser_scale = teaser_scale
        self.num_teasers=num_teasers
        self.ajaxified = ajaxified
        self.show_title=show_title
        self.show_description=show_description
        self.search_base = search_base
        self.uid = uuid.uuid4()

    def _get_header(self):
        if not hasattr(self, '_header'):
            self._header = u''
        return self._header

    def _set_header(self, header):
        self._header = header

    # B/C header was added - ensure existing teaser portlets still work.
    header = property(_get_header, _set_header)

    def _get_display_columns(self):
        if not hasattr(self, '_display_columns'):
            self._display_columns = u'1'
        return self._display_columns

    def _set_display_columns(self, columns):
        self._display_columns = columns

    # B/C display_columns was added - ensure existing teaser portlets still
    #     work.
    display_columns = property(_get_display_columns, _set_display_columns)

    @property
    def title(self):
        return self.header or _(u'portlet_teaser_title', default=u"Teaser")


class AddForm(base.AddForm):
    form_fields = form.Fields(ITeaserPortlet)
    #fields['search_base'].widgetFactory = ContentTreeFieldWidget
    label = _(u'portlet_label_add', default=u"Add portlet to show teasers.")
    description = _(u'portlet_help_add', default=u"This portlet shows teasers.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ITeaserPortlet)
    #fields['search_base'].widgetFactory = ContentTreeFieldWidget
    label = _(u'portlet_label_add', default=u"Add portlet to show teasers.")
    description = _(u'portlet_help_add', default=u"This portlet shows teasers.")
