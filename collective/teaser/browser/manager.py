# -*- coding: utf-8 -*-
from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.teaser.interfaces import ITeaserPortletManager


class TeaserPortletManagerRenderer(ColumnPortletManagerRenderer):
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, ITeaserPortletManager)
    template = ViewPageTemplateFile('teaser_portlet_renderer.pt')