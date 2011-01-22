from zope.interface import implements
try:
    from Products.LinguaPlone import public  as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
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
     atapi.StringField('url',
        required=True,
        searchable=False,
        languageIndependent=True,
		validators=("isURL"),
		widget = atapi.StringWidget(
            label = _(u"Url"),
			description = _(u"Use the form http://WEBSITE.TLD/"),
        ),
	),
	atapi.TextField('text',
        required=False,
        searchable=False,
        languageIndependent=False,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
		widget = atapi.RichWidget(
            label = _(u"Text"),
			description = _(u"Additional notes"),
			rows = 5,
            allow_file_upload=False,
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
