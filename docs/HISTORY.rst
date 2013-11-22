
Changelog
=========

2.3 (2013-11-23)
----------------

- Add an upgrade helper for old, pre 2.0 collective.teaser portlets by adding
  a dummy Assignment class to common.py.
  [thet]

- Don't restrict to only published teasers. Also show unpublished for users
  with appropriate permissions.
  [thet]

- Just cache portlet rendering on request instead of custom cachekey function.
  [thet]

2.2
---

- Fix Unicode.
  [rnix, 2012-09-26]

- Fix use in conjunction with ``collective.lineage``.
  [rnix, 2012-09-25]

- Fix portlet assignment lookup.
  [rnix, 2012-09-25]

- Add ``display_columns`` for teaser portlet.
  [rnix, 2012-08-16]

- Add portlet header for teaser portlet.
  [rnix, 2012-08-16]

2.1
---

- Fix HTML validation error - div not allowed as direct descendent of dl.
  [thet]


2.0
---

- Configurable search path of teaser portlet.
  [rnix]


2.0b1
-----

- Remove IPortletAvailable adapter, which was a overcomponentized
  proof-of-concept and too complicated to be used.
  [thet]

- Remove alternative image field, which was meant to allow a portlet to select
  an Landscape/Portrait image from the same teaser. The meaning of the option
  was unclear. Instead, upload two different Teasers and select different
  importance levels for it.
  [rnix, thet]

- Option to get Teasers via AJAX call. This makes the teaser portlet better
  cachable.
  [rnix]


1.0
---

- Remove text field and use optionally the description field instead.
  [thet]

- Add Teaser to image_types in portal_atct to allow image scale recreation.
  [thet]

- Add HistroyAwareMixin and configure Teaser to be versionable.
  [thet]

- Initial release
