# -*- coding: utf-8 -*-
import random
from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName


def _teaserlist(context, data):
    """XXX: cache on request.
    """
    context = aq_inner(context)
    cat = getToolByName(context,'portal_catalog')
    query = {}
    query['Type'] = 'Teaser'

    # show only selected importances
    query['importance'] = data.importance_levels

    # show only published and not expired, even for admins
    query['review_state'] = 'published'
    query['effectiveRange'] = DateTime()
    brains = cat(**query)

    # make a weighted (multiplied by importance) list of teasers.
    teasers = []
    [teasers.extend(int(brain.importance) * [brain]) for brain in brains]
    return teasers


def get_teasers(context, data, request):
    teasers = _teaserlist(context, data)
    if not teasers: return None

    # get used id's from request and exclude them
    taken_teasers = getattr(request, 'teasers', [])

    choosen_teasers = []
    for cnt in range(data.num_teasers):
        # reduce selected teasers with all taken_teasers
        teasers = [_ for _ in teasers if _.id not in taken_teasers]
        if not teasers:
            break

        # randomly select num_teasers from all
        choosen_teaser = random.choice(teasers)
        choosen_teasers.append(choosen_teaser.getObject())
        taken_teasers.append(choosen_teaser.id)

    # save new taken teaser list in request
    request['teasers'] = taken_teasers

    # create data structure and return
    scale = data.teaser_scale
    show_title = data.show_title
    show_desc = data.show_description
    return [
        {
            'title': show_title and teaser.title or None,
            'image': getattr(teaser, 'image', False) \
                         and teaser.getField('image').tag(
                             teaser,
                             scale=scale,
                             alt=teaser.title,
                             title=teaser.title) or None,
             'description': show_desc and teaser.Description() or None,
             'url': teaser.getLink_internal() \
                        and teaser.getLink_internal().absolute_url() \
                        or teaser.link_external or None,
        }
        for teaser in choosen_teasers
    ]
