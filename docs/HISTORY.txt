Changelog
=========

2.0b1 (unreleased)
-------------------

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


1.0dev (unreleased)
-------------------

- Remove text field and use optionally the description field instead.
  [thet]

- Add Teaser to image_types in portal_atct to allow image scale recreation.
  [thet]

- Add HistroyAwareMixin and configure Teaser to be versionable.
  [thet]

- Initial release
