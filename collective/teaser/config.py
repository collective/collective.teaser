PROJECTNAME = "collective.teaser"
DEFAULT_IMPORTANCE = "3"
ADD_PERMISSIONS = {
    "Teaser"        : "collective.teaser: Add Teaser",
}

from Products.CMFCore.permissions import setDefaultRoles
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Owner', 'Contributor'))


from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from collective.teaser import MsgFact as _

def ImportanceVocabulary(context):
    items =[(_(u"Highest importance"),'1'),
           (_(u"High importance"),'2'),
           (_(u"Normal importance"),'3'),
           (_(u"Low importance"),'4'),
           ]
    return SimpleVocabulary.fromItems(items)
directlyProvides(ImportanceVocabulary, IVocabularyFactory)
