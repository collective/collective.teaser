from zope.interface import Interface, Attribute


class IPortletAvailable(Interface):
    """Interface for Adapters, implementing logic to determine, if the
    Teaserportlet should be shown or not.
    """
    portlet = Attribute(u"""The portlet assignment""")
    
    manager = Attribute(u"""The portlet manager""")
    
    context = Attribute(u"""The context, this portlet is shown""")


class ITeaser(Interface):
    """ Marker interface
    """