# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "collective.teaser"
DEFAULT_IMPORTANCE = '3',
ADD_PERMISSIONS = {
    "Teaser": "collective.teaser: Add Teaser",
}

DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(
    DEFAULT_ADD_CONTENT_PERMISSION,
    ('Manager', 'Owner', 'Contributor')
)
