from plone.memoize.ram import global_cache

def cache_invalidate_teaserlist(obj, event):
    """ Invalidate the _teaserlist cache after updating or adding a teaser.
    """
    print "INVALIDATE"
    global_cache.invalidate(
            'collective.teaser.browser.common.Renderer._teaserlist')
