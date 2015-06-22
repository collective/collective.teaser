# -*- coding: utf-8 -*-
from collective.teaser.interfaces import ITeaserPortletManager
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


@adapter(Interface, IDefaultBrowserLayer, IBrowserView, ITeaserPortletManager)
class TeaserPortletManagerRenderer(ColumnPortletManagerRenderer):
    template = ViewPageTemplateFile('teaser_portlet_manager_renderer.pt')
