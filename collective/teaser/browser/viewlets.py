# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from Acquisition import (
    aq_inner,
    aq_parent,
)
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName


class TeaserPortletsViewlet(ViewletBase):

    name = 'Teaser portlets'
    manage_view = '@@manage-teaserportlets'

    @property
    def display(self):
        return True
    
    def update(self):
        if not self.display:
            self.canManagePortlets = False
            return
        context_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_context_state')
        self.manageUrl = '%s/%s' % (context_state.view_url(), self.manage_view)
        # This is the way it's done in plone.app.portlets.manager, so we'll 
        # do the same
        mt = getToolByName(self.context, 'portal_membership')
        self.canManagePortlets = mt.checkPermission(
            'Portlets: Manage portlets', self.context)