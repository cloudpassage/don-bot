Changelog
=========

v0.18.0 (2018-05-07)
--------------------

Changes
~~~~~~~

- Move testing to a separate step in the Docker build process. [Ash
  Wilson]

Other
~~~~~

- Rev donbot to 0.18.0 and celery to 0.7.0. [Jye Lee]

- Encrypt HALO_API_KEY AND HALO_API_SECRET_KEY to travis.yml. [Jye Lee]

v0.17.6 (2018-04-12)
--------------------

- Rev halocelery to v0.6.0 in Dockerfile. [Jye Lee]

- Rev __init__.py to 0.17.6. [Jye Lee]

- Donbot/issues/38: Test use api last event as start instead of craft
  crafted timestamps has a chance to make the grid barf with a 422.
  reasons unknown. wasn't able to reproduce using the crafted timestamp
  but sean's donbot crashed continuously with the 422. [Jye Lee]

- Update readme with create a slack bot user. [Jye Lee]

v0.17.5 (2018-04-10)
--------------------

- Version rev to v0.17.5. [Jye Lee]

- Issue/26: Add config setup instructions to donbot config. [Jye Lee]

- Donbot/issues/33: use grouped hash. [Jye Lee]

  donbot/issues/33: update quarantine integration test

- Donbot/issue/28 rename OCTOBOX to Halo Cortex for file uploads. [Jye
  Lee]

v0.17.4 (2018-03-27)
--------------------

- V0.17.4. [Jye Lee]

- Rev to halocelery 0.5.0. [Jye Lee]

v0.17.3 (2018-03-23)
--------------------

- Fixed sytax error. [Hana Lee]

- Fixed ipblocker_enable. [Hana Lee]

- V0.17.3. [Hana Lee]

- Fixed the logic and syntax. [Hana Lee]

- Added check quarantine_enable and ipblocker_enable added suppress
  events. [Hana Lee]

- Removed debug message. [Hana Lee]

- Added config_helper to ipblocker.py. [Hana Lee]

- Created config_helper for cortexlib. [Hana Lee]

- Removed yml and env file from donbot. [Hana Lee]

- Read env before cortex_conf. [Hana Lee]

- Updated halocelery version to v0.4.9. [Hana Lee]

v0.17.2 (2018-03-20)
--------------------

- Updated Dockerfile to use the latest halocelery. [Hana Lee]

- Updated version in __init__.py. [Hana Lee]

- Test: name change from octo to cortex. [Jye Lee]

- CS-487 .encode qstring. [Jye Lee]

- Added test for servers_by_cve in lexical added documentation for CVE
  search in help_text. [Hana Lee]

- Changed syntax error. [Hana Lee]

- Added task - servers_by_cve. [Hana Lee]

- Migrate octobox bot to donbot. [Jye Lee]

v0.17.0 (2017-06-08)
--------------------

- Tuned down the threads. [mong2]

v0.16.0 (2017-01-31)
--------------------

New
~~~

- Container will exit on component failure.  We expect that the
  container will be started with "--restart always". [Ash Wilson]

Changes
~~~~~~~

- Improved in-channel message formatting consistency. [Ash Wilson]

v0.15.1 (2017-01-24)
--------------------

Changes
~~~~~~~

- Correcting package metadata. [Ash Wilson]

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


