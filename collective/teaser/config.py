from Products.CMFCore.permissions import setDefaultRoles
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from collective.teaser import MsgFact as _
from plone.app.imaging.utils import getAllowedSizes

PROJECTNAME = "collective.teaser"
DEFAULT_IMPORTANCE = "3"
ADD_PERMISSIONS = {
    "Teaser"        : "collective.teaser: Add Teaser",
}

DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Owner', 'Contributor'))


def ImportanceVocabulary(context):
    items =[(_(u"Highest importance"),'1'),
           (_(u"High importance"),'2'),
           (_(u"Normal importance"),'3'),
           (_(u"Low importance"),'4'),
           ]
    return SimpleVocabulary.fromItems(items)
directlyProvides(ImportanceVocabulary, IVocabularyFactory)

def ImageScaleVocabulary(context):
    allowed_sizes = getAllowedSizes()
    items = [("%s(%s, %s)" %(key, value[0], value[1]), key)
        for key,value in allowed_sizes if allowed_sizes]
    return SimpleVocabulary.fromItems(items)
directlyProvides(ImageScaleVocabulary, IVocabularyFactory)
