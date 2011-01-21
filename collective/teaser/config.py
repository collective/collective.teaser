PROJECTNAME = "collective.teaser"
ADD_PERMISSIONS = {
    "Teaser"        : "collective.teaser: Add Teaser",
}

from Products.CMFCore.permissions import setDefaultRoles
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION,
                ('Manager', 'Owner', 'Contributor'))
