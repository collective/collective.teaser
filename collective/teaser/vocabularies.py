from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from collective.teaser import MsgFact as _
from plone.app.imaging.utils import getAllowedSizes


def ImportanceVocabulary(context):
    items =[
        (_(u"importance_highest", default=u"Highest importance"),'4'),
        (_(u"importance_high", default=u"High importance"),'3'),
        (_(u"importance_normal", default=u"Normal importance"),'2'),
        (_(u"importance_low", default=u"Low importance"),'1')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(ImportanceVocabulary, IVocabularyFactory)


def ImageScaleVocabulary(context):
    allowed_sizes = getAllowedSizes()
    items = [(u'%s(%s, %s)' %(key, value[0], value[1]), key)
        for key,value in allowed_sizes.items() if allowed_sizes]
    return SimpleVocabulary.fromItems(items)

directlyProvides(ImageScaleVocabulary, IVocabularyFactory)


def ExcludeScaleVocabulary(context):
    items =[
        (_(u"exclude_vertical", default=u"Exclude vertical Images"),'exclude_vertical'),
        (_(u"exclude_horizontal", default=u"Exclude horizontal Images"),'exclude_horizontal'),
        (_(u"exclude_quadratic", default=u"Exclude Quadratic Images"),'exclude_quadratic')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(ExcludeScaleVocabulary, IVocabularyFactory)


def PortletLayoutVocabulary(context):
    items =[
        (_(u"layout_vertical", default=u"Vertical portlet"),'layout_vertical'),
        (_(u"layout_horizontal", default=u"Horizontal portlet"),'layout_horizontal'),
        (_(u"layout_quadratic", default=u"Quadratic portlet"),'layout_quadratic')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(ExcludeScaleVocabulary, IVocabularyFactory)
