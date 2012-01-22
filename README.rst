collective.teaser
=================

Teaser/Banner content type for Plone

This Plone add-on installs the content type teaser, which is meant to be used
for small advertisements on a homepage to advertise own or external content.

Randomly selected teasers will be shown in a Teaser portlet. An importance
level controls the frequency, how often teasers are shown - a teaser with
higher importance will be shown more frequently. If more teasers are shown in
portlets on a page, one teaser isn't shown twice.

If you need to show specific teasers only in specific portlets (e.g. to
distinguish between horizontal and vertical teasers), use the importance levels
or subject filter to assign teasers to those portlets.

If you need to hide the teaser's title or description (latter is only shown, if
it's defined), customize the teaser template with z3c.jbot or do some css
styling.


TODO
----
* Ajax deferring does not easily work with Diazo. Maybe integrate 'ajax_load'
  in request.form parameters (see plone.app.theming). 

* When the teaser is going to be displayed on a default page, the teaser is
  called twice. This seems to be a bug/default-page-sideeffect in Plone.
  When only one teaser is available for that portlet, on the second call it's
  removed from the available teasers, since it's already in the taken_teasers
  list. As a result, no teaser is shown. A workaround would be to cache the
  call to get the teasers list with plone.app.portlets.cache.render_cachekey.
  Only, that method is already a instance_property, caching with plone.memoize
  fails.

Copyright
---------

Johannes Raggam, BlueDynamics Alliance - Author
Robert Niederreiter, BlueDynamics Alliance - Contributions
