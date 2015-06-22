# -*- coding: utf-8 -*-
from plone.app.imaging.utils import getAllowedSizes
from zope.i18nmessageid import MessageFactory
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

_ = MessageFactory('collective.teaser')


def ImportanceVocabulary(context):
    items = [
        (_(u"importance_highest", default=u"Highest importance"), '4'),
        (_(u"importance_high", default=u"High importance"), '3'),
        (_(u"importance_normal", default=u"Normal importance"), '2'),
        (_(u"importance_low", default=u"Low importance"), '1')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(ImportanceVocabulary, IVocabularyFactory)


def ImageScaleVocabulary(context):
    allowed_sizes = getAllowedSizes()
    items = [
        (u'%s(%s, %s)' % (key, value[0], value[1]), key)
        for key, value in allowed_sizes.items() if allowed_sizes
    ]
    return SimpleVocabulary.fromItems(items)

directlyProvides(ImageScaleVocabulary, IVocabularyFactory)
