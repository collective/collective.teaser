from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from collective.teaser import MsgFact as _
from plone.app.imaging.utils import getAllowedSizes

def ImportanceVocabulary(context):
    items =[(_(u"Highest importance"),'4'),
           (_(u"High importance"),'3'),
           (_(u"Normal importance"),'2'),
           (_(u"Low importance"),'1'),
           ]
    return SimpleVocabulary.fromItems(items)
directlyProvides(ImportanceVocabulary, IVocabularyFactory)

def ImageScaleVocabulary(context):
    allowed_sizes = getAllowedSizes()
    items = [(u'%s(%s, %s)' %(key, value[0], value[1]), key)
        for key,value in allowed_sizes.items() if allowed_sizes]
    return SimpleVocabulary.fromItems(items)
directlyProvides(ImageScaleVocabulary, IVocabularyFactory)
