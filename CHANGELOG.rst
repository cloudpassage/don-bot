Changelog
=========

v0.13.1
-------

Changes
~~~~~~~

- Removed unnecessary print statement. [Ash Wilson]

v0.13 (2016-12-19)
------------------

New
~~~

- Added last event timestamp to health query response. [Ash Wilson]

- Added health query. [Ash Wilson]

Changes
~~~~~~~

- Improved API error handling for connection errors. [Ash Wilson]

Fix
~~~

- Case-insensitive match for bot name  closes #1. [Ash Wilson]

- Corrected issue with repeated messages delivered to Slack because
  timestamp query is inclusive. [Ash Wilson]

- Consolidated health report into main() to ease checking of thread
  health. [Ash Wilson]

- Wait instead of fail if events query comes back empty. [Ash Wilson]

v0.12.1 (2016-12-14)
--------------------

Changes
~~~~~~~

- Updated instructions to pull container from Dockerhub directly,
  instead of building locally. [Ash Wilson]

v0.12 (2016-12-12)
------------------

New
~~~

- Added "config" and "version" to bot commands. [Ash Wilson]

- Bot can monitor Halo API for critical events. [Ash Wilson]

Changes
~~~~~~~

- Added health checker and more meaningful application logs. [Ash
  Wilson]

- Adding bot profile image. [Ash Wilson]

v0.11 (2016-12-05)
------------------

New
~~~

- Added LIDS policies to group report. [Ash Wilson]

v0.10 (2016-12-04)
------------------

Changes
~~~~~~~

- Version 0.10.  Many internal refactors, better general quality and
  error handling. [Ash Wilson]

v0.9 (2016-12-03)
-----------------

New
~~~

- First working commit of Don-Bot BETA. [Ash Wilson]


