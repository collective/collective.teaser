from zope.interface import (
    Interface,
    Attribute,
)
from plone.portlets.interfaces import IPortletManager


class ITeaser(Interface):
    """Marker interface.
    """

class ITeaserLayer(Interface):
    """Browser Layer for teaser.
    """

class IPortletAvailable(Interface):
    """Interface for Adapters, implementing logic to determine, if the
    Teaserportlet should be shown or not.
    """
    portlet = Attribute(u"""The portlet assignment""")

    manager = Attribute(u"""The portlet manager""")

    context = Attribute(u"""The context, this portlet is shown""")

class ITeaserPortletManager(IPortletManager):
    """The IColumn bit means that we can add all the portlets available to
    the right-hand and left-hand column portlet managers
    """
