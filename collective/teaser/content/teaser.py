from zope.interface import implements
try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from collective.teaser.interfaces import ITeaser
from collective.teaser.config import PROJECTNAME, DEFAULT_IMPORTANCE
from collective.teaser import MsgFact as _

from plone.app.imaging.utils import getAllowedSizes
allowed_sizes = getAllowedSizes()

type_schema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.ImageField('image',
        required=False,
        languageIndependent=True,
        sizes = allowed_sizes,
        widget=atapi.ImageWidget(
            label=_(u"Image"),
            description=_(u"Image to display as teaser."),
            ),
        ),
     atapi.ImageField('altimage',
        required=False,
        languageIndependent=True,
        sizes = allowed_sizes,
        widget=atapi.ImageWidget(
            label=_(u"Alternative image"),
            description=_(u"Alternative image in different layout, e.g. in portrait instead of landscape layout. A portlet can prefer alternative layouts."),
            ),
        ),
     atapi.ReferenceField('link_internal',
        required=False,
        searchable=False,
        languageIndependent=True,
		multiValued=False,
        relationship='ref_link_internal',
        widget = ReferenceBrowserWidget(
            label = _(u"Link to Internal Content"),
			description = _(u"Link to internal content. For external content, use the field below."),
            allow_search=True,
            allow_browse=True,
            force_close_on_insert = True,
            startup_directory = '/',
            #show_results_without_query = True,
            #show_review_state = True,
        ),
	),
    atapi.StringField('link_external',
        required=False,
        searchable=False,
        languageIndependent=True,
		validators=("isURL"),
		widget = atapi.StringWidget(
            label = _(u"Link to external Content"),
			description = _(u"Url to external content. For internal content, use the field above. Use the form http://WEBSITE.TLD/"),
        ),
	),
	atapi.TextField('text',
        required=False,
        searchable=False,
        languageIndependent=False,
        default_content_type = 'text/plain',
        allowable_content_types = ('text/plain',),
		widget = atapi.TextAreaWidget(
            label = _(u"Text"),
			description = _(u"Additional notes"),
			rows = 5,
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
            label = _(u"Importance"),
			description = _(u"Select the importance of the teaser. The frequency of the teaser will be set accordingly."),
        ),
	),

))

type_schema['description'].widget.visible = {'view': 'invisible',
                                             'edit': 'invisible'}

schemata.finalizeATCTSchema(type_schema,
                            folderish=False,
                            moveDiscussion=False)

class Teaser(base.ATCTContent):
    # security = ClassSecurityInfo()
    implements(ITeaser)

    portal_type = "Teaser"
    _at_rename_after_creation = True
    schema = type_schema

atapi.registerType(Teaser, PROJECTNAME)
