Changelog
=========

.. towncrier release notes start

0.3.0 (2023-08-16)
==================

Features
--------

* Layout nodes can now track the minimum permitted layout size in addition to the current actual layout size. (`#78 <https://github.com/beeware/travertino/issues/78>`_)


Backward Incompatible Changes
-----------------------------

* Support for Python 3.7 was removed. (`#80 <https://github.com/beeware/travertino/issues/80>`_)


Misc
----

* `#44 <https://github.com/beeware/travertino/issues/44>`_, `#45 <https://github.com/beeware/travertino/issues/45>`_, `#46 <https://github.com/beeware/travertino/issues/46>`_, `#47 <https://github.com/beeware/travertino/issues/47>`_, `#48 <https://github.com/beeware/travertino/issues/48>`_, `#49 <https://github.com/beeware/travertino/issues/49>`_, `#50 <https://github.com/beeware/travertino/issues/50>`_, `#51 <https://github.com/beeware/travertino/issues/51>`_, `#52 <https://github.com/beeware/travertino/issues/52>`_, `#53 <https://github.com/beeware/travertino/issues/53>`_, `#54 <https://github.com/beeware/travertino/issues/54>`_, `#55 <https://github.com/beeware/travertino/issues/55>`_, `#56 <https://github.com/beeware/travertino/issues/56>`_, `#57 <https://github.com/beeware/travertino/issues/57>`_, `#58 <https://github.com/beeware/travertino/issues/58>`_, `#59 <https://github.com/beeware/travertino/issues/59>`_, `#60 <https://github.com/beeware/travertino/issues/60>`_, `#61 <https://github.com/beeware/travertino/issues/61>`_, `#62 <https://github.com/beeware/travertino/issues/62>`_, `#63 <https://github.com/beeware/travertino/issues/63>`_, `#65 <https://github.com/beeware/travertino/issues/65>`_, `#66 <https://github.com/beeware/travertino/issues/66>`_, `#67 <https://github.com/beeware/travertino/issues/67>`_, `#72 <https://github.com/beeware/travertino/issues/72>`_, `#73 <https://github.com/beeware/travertino/issues/73>`_, `#74 <https://github.com/beeware/travertino/issues/74>`_, `#75 <https://github.com/beeware/travertino/issues/75>`_, `#76 <https://github.com/beeware/travertino/issues/76>`_, `#77 <https://github.com/beeware/travertino/issues/77>`_, `#79 <https://github.com/beeware/travertino/issues/79>`_, `#81 <https://github.com/beeware/travertino/issues/81>`_, `#82 <https://github.com/beeware/travertino/issues/82>`_, `#83 <https://github.com/beeware/travertino/issues/83>`_, `#84 <https://github.com/beeware/travertino/issues/84>`_, `#85 <https://github.com/beeware/travertino/issues/85>`_, `#86 <https://github.com/beeware/travertino/issues/86>`_, `#87 <https://github.com/beeware/travertino/issues/87>`_


0.2.0 (2023-03-24)
==================

Features
--------

* Node now supports the ``clear`` method in order to clear all children. (`#23 <https://github.com/beeware/travertino/issues/23>`_)
* Constants for absolute and relative font sizing were added. (`#43 <https://github.com/beeware/travertino/issues/43>`_)


Bugfixes
--------

* Handling of ``none`` as a property value has been corrected. (`#3 <https://github.com/beeware/travertino/issues/3>`_)


Improved Documentation
----------------------

* Details on towncrier and pre-commit ussage were added to the README. (`#18 <https://github.com/beeware/travertino/issues/18>`_)


Misc
----

* `#22 <https://github.com/beeware/travertino/issues/22>`_, `#24 <https://github.com/beeware/travertino/issues/24>`_, `#25 <https://github.com/beeware/travertino/issues/25>`_, `#26 <https://github.com/beeware/travertino/issues/26>`_, `#30 <https://github.com/beeware/travertino/issues/30>`_, `#34 <https://github.com/beeware/travertino/issues/34>`_, `#35 <https://github.com/beeware/travertino/issues/35>`_, `#36 <https://github.com/beeware/travertino/issues/36>`_, `#37 <https://github.com/beeware/travertino/issues/37>`_, `#38 <https://github.com/beeware/travertino/issues/38>`_, `#39 <https://github.com/beeware/travertino/issues/39>`_, `#40 <https://github.com/beeware/travertino/issues/40>`_, `#41 <https://github.com/beeware/travertino/issues/41>`_, `#42 <https://github.com/beeware/travertino/issues/42>`_


0.1.3 (2020-05-25)
------------------

Features
^^^^^^^^

* Introduced some constants used by Pack that have more general uses. (`#5 <https://github.com/beeware/travertino/issues/5>`_)
* Added the ability to add, insert and remove children from a node tree. (`#10 <https://github.com/beeware/travertino/issues/10>`_)
* Added color validation in rgba and hsla constructors (`#17 <https://github.com/beeware/travertino/issues/17>`_)
* Added support for declaring a system default font size. (`#19 <https://github.com/beeware/travertino/issues/19>`_)

Misc
^^^^

* `#15 <https://github.com/beeware/travertino/issues/15>`_, `#16 <https://github.com/beeware/travertino/issues/16>`_


0.1.2
-----
* Added constants for system and message fonts
* Added hash method to fonts and colors

0.1.1
-----

* Added font definitions

0.1.0
-----

Initial release.
