from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content import base, image, schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from collective.teaser.interfaces import ITeaser
from collective.teaser.config import PROJECTNAME, DEFAULT_IMPORTANCE
from collective.teaser import MsgFact as _
from plone.app.imaging.utils import getAllowedSizes


allowed_sizes = getAllowedSizes()


type_schema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.ImageField('image',
        required=False,
        languageIndependent=True,
        sizes=allowed_sizes,
        widget=atapi.ImageWidget(
            label=_(u"label_image", default=u"Image"),
            description=_(u"help_image",
                          default=u"Image to display as teaser."),
        ),
    ),

    atapi.ReferenceField('link_internal',
        required=False,
        searchable=False,
        languageIndependent=True,
        multiValued=False,
        relationship='ref_link_internal',
        widget=ReferenceBrowserWidget(
            label=_(u"label_link_internal", default=u"Internal Link"),
            description=_(u"help_link_internal",
                          default=u"Link to internal content. For external " +\
                                  u"content, use the External Link field."),
            allow_search=True,
            allow_browse=True,
            force_close_on_insert = True,
            startup_directory = '/',
        ),
    ),

    atapi.StringField('link_external',
        required=False,
        searchable=False,
        languageIndependent=True,
        validators=("isURL"),
        widget=atapi.StringWidget(
            label=_(u"label_link_external", default=u"External Link"),
            description=_(u"help_link_external",
                          default=u"Url to external content. For internal " +\
                                  u"content, use the field above. Use the " +\
                                  u"form http://WEBSITE.TLD/"),
        ),
    ),

    atapi.StringField('importance',
        required=True,
        searchable=True,
        languageIndependent=True,
        vocabulary_factory="collective.teaser.ImportanceVocabulary",
        enforceVocabulary=True,
        default=DEFAULT_IMPORTANCE,
        widget=atapi.SelectionWidget(
            label=_(u"label_importance", default=u"Importance"),
            description=_(u"help_importance",
                          default=u"Select the importance of the teaser. " +\
                                  u"The frequency of the teaser will be " +\
                                  u"set accordingly."),
        ),
    ),
))

type_schema['description'].widget.visible = {
    'view': 'invisible',
    'edit': 'invisible',
}

schemata.finalizeATCTSchema(type_schema,
                            folderish=False,
                            moveDiscussion=False)


class Teaser(base.ATCTContent, image.ATCTImageTransform, HistoryAwareMixin):
    implements(ITeaser)
    portal_type = "Teaser"
    _at_rename_after_creation = True
    schema = type_schema
    security = ClassSecurityInfo()

    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            kwargs['title'] = self.title
        return self.getField('image').tag(self, **kwargs)

atapi.registerType(Teaser, PROJECTNAME)
