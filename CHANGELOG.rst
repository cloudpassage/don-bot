Changelog
=========

v0.15.0 (2017-01-23)
--------------------

New
~~~

- Now includes server EC2 metadata, when available. [Ash Wilson]

- Don-Bot now only responds to requests from users who are a member of
  the configured SLACK_CHANNEL, which defaults to #halo. [Ash Wilson]

v0.13.2 (2017-01-09)
--------------------

New
~~~

- Added last event timestamp to health query response. [Ash Wilson]

- Added health query. [Ash Wilson]

- Added "config" and "version" to bot commands. [Ash Wilson]

- Bot can monitor Halo API for critical events. [Ash Wilson]

- Added LIDS policies to group report. [Ash Wilson]

- First working commit of Don-Bot BETA. [Ash Wilson]

Changes
~~~~~~~

- Improving status messaging. [Ash Wilson]

- Removed unnecessary print statement. [Ash Wilson]

- Improved API error handling for connection errors. [Ash Wilson]

- Updated instructions to pull container from Dockerhub directly,
  instead of building locally. [Ash Wilson]

- Added health checker and more meaningful application logs. [Ash
  Wilson]

- Adding bot profile image. [Ash Wilson]

- Version 0.10.  Many internal refactors, better general quality and
  error handling. [Ash Wilson]

Fix
~~~

- Case-insensitive match for bot name  closes #1. [Ash Wilson]

- Corrected issue with repeated messages delivered to Slack because
  timestamp query is inclusive. [Ash Wilson]

- Consolidated health report into main() to ease checking of thread
  health. [Ash Wilson]

- Wait instead of fail if events query comes back empty. [Ash Wilson]


