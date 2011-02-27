from zope.interface import Interface

class ITeaser(Interface):
    """ Marker interface
    """

class ITeaserAvailable(Interface):
    """ Interface for Adapters, implementing logic to determine, if the
        Teaserportlet should be shown or not.
    """
