# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.interfaces import IPortletPermissionChecker
from z3c.form import button
from z3c.form import form
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(IPortletAddForm)
class AddForm(form.AddForm):

    label = _(u"Configure portlet")

    def add(self, object):
        ob = self.context.add(object)
        self._finishedAdd = True
        return ob

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        addview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(addview))
        # XXX no idea why its written this way down, but better keep
        # no one writes it that strange w/o reason
        url = str(
            getMultiAdapter(
                (context, self.request),
                name=u"absolute_url"
            )
        )
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(
        _(u"label_cancel", default=u"Cancel"),
        name='cancel_add'
    )
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''


@implementer(IPortletEditForm)
class EditForm(form.EditForm):
    """An edit form for portlets.
    """

    label = _(u"Modify portlet")

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        # XXX no idea why its written this way down, but better keep
        # no one writes it that strange w/o reason
        url = str(
            getMultiAdapter(
                (context, self.request),
                name=u"absolute_url"
            )
        )
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''
