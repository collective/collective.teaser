from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager


class ITeaser(Interface):
    """Marker interface.
    """

class ITeaserLayer(Interface):
    """Browser Layer for teaser.
    """

class ITeaserPortletManager(IPortletManager):
    """Teaser Portlet Manager
    """
