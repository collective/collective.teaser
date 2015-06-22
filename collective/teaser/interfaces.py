# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletManager
from zope.interface import Interface


class ITeaser(Interface):
    """Marker interface.
    """


class ITeaserLayer(Interface):
    """Browser Layer for teaser.
    """


class ITeaserPortletManager(IPortletManager):
    """Teaser Portlet Manager
    """
