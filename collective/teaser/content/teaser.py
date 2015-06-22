# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from collective.teaser.config import DEFAULT_IMPORTANCE
from collective.teaser.config import PROJECTNAME
from collective.teaser.interfaces import ITeaser
from plone.app.imaging.utils import getAllowedSizes
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import image
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.CMFCore.permissions import View
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi

_ = MessageFactory('collective.teaser')

allowed_sizes = getAllowedSizes()

type_schema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.ImageField(
        'image',
        required=False,
        languageIndependent=True,
        sizes=allowed_sizes,
        widget=atapi.ImageWidget(
            label=_(u"label_image", default=u"Image"),
            description=_(
                u"help_image",
                default=u"Image to display as teaser."
            ),
        ),
    ),

    atapi.ReferenceField(
        'link_internal',
        required=False,
        searchable=False,
        languageIndependent=True,
        multiValued=False,
        relationship='ref_link_internal',
        widget=ReferenceBrowserWidget(
            label=_(u"label_link_internal", default=u"Internal Link"),
            description=_(
                u"help_link_internal",
                default=u"Link to internal content. For external "
                        u"content, use the External Link field."),
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory='/',
        ),
    ),

    atapi.StringField(
        'link_external',
        required=False,
        searchable=False,
        languageIndependent=True,
        validators=("isURL"),
        widget=atapi.StringWidget(
            label=_(u"label_link_external", default=u"External Link"),
            description=_(
                u"help_link_external",
                default=u"Url to external content. For internal content, "
                        u"use the field above. Use form http://WEBSITE.TLD/"
            ),
        ),
    ),

    atapi.StringField(
        'importance',
        required=True,
        searchable=True,
        languageIndependent=True,
        vocabulary_factory="collective.teaser.ImportanceVocabulary",
        enforceVocabulary=True,
        default=DEFAULT_IMPORTANCE,
        widget=atapi.SelectionWidget(
            label=_(u"label_importance", default=u"Importance"),
            description=_(
                u"help_importance",
                default=u"Select the importance of the teaser. "
                        u"The frequency of the teaser will be "
                        u"set accordingly."),
        ),
    ),
))

schemata.finalizeATCTSchema(
    type_schema,
    folderish=False,
    moveDiscussion=False
)


@implementer(ITeaser)
class Teaser(base.ATCTContent, image.ATCTImageTransform, HistoryAwareMixin):
    portal_type = "Teaser"
    _at_rename_after_creation = True
    schema = type_schema
    security = ClassSecurityInfo()

    @security.protected(View)
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.title.encode('utf-8')
        return self.getField('image').tag(self, **kwargs)

atapi.registerType(Teaser, PROJECTNAME)
