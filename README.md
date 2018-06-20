# Don-Bot, the Halo Slackbot

[![Build Status](https://travis-ci.org/cloudpassage/don-bot.svg?branch=master)](https://travis-ci.org/cloudpassage/don-bot)
[![Code Climate](https://codeclimate.com/github/cloudpassage/don-bot/badges/gpa.svg)](https://codeclimate.com/github/cloudpassage/don-bot)
[![Issue Count](https://codeclimate.com/github/cloudpassage/don-bot/badges/issue_count.svg)](https://codeclimate.com/github/cloudpassage/don-bot)
[![Test Coverage](https://codeclimate.com/github/cloudpassage/don-bot/badges/coverage.svg)](https://codeclimate.com/github/cloudpassage/don-bot/coverage)

https://store.docker.com/community/images/halotools/don-bot

![Don Bot](http://www.cloudpassage.com/wp-content/uploads/2016/12/don-operator.png)

## Summary

This is a chatbot that allows you to query your CloudPassage Halo account
without leaving the comfort of your Slack client.  No need to log into the
web portal to find out the status of a server- just
`donbot tell me about server XYZ`.

Donbot sends messages to the #halo channel by default, or whatever you have
specified by the ${SLACK_CHANNEL} environment variable.  Only users who are in
that channel will be able to interrogate Don-Bot.  Requests from any user who
is not a member of the #halo channel (or ${SLACK_CHANNEL}, if you overrode the
default channel) will be ignored.  Consider making that channel private,
unless you want everyone in your Slack domain to be able to access Halo through
the bot.

It lives in a Docker container, so you can deploy pretty much anywhere.
No listening ports, it just establishes a connection to Slack and listens
for messages where it's name is mentioned. Then it reaches out to the
CloudPassage Halo API to gather information, and drops a report back into the
channel where it was requested.

This bot can optionally poll the Halo API events endpoint, and post all
critical events into the configured channel.  See below for details...


Use a read-only CloudPassage Halo API key...

### Running Don-Bot

Requirements:

* CloudPassage Halo READ-ONLY API key
* Slack chatbot token (don-operator.png included in repo for bot profile image)
* An instance of Halo Celery running. (https://hub.docker.com/r/halotools/halocelery)

Doing the thing:

Set the following env vars, and then run:

| var                  | purpose                                               |
|----------------------|-------------------------------------------------------|
| CELERY_BACKEND_URL   | Url for Celery backend                                |
| CELERY_BROKER_URL    | Url for Celery broker                                 |
| FLOWER_HOST          | Url for Flower host                                   |
| HALO_API_KEY         | Halo API key ID (read-only)                           |
| HALO_API_SECRET_KEY  | Halo API secret                                       |
| SLACK_API_TOKEN      | Slack token for bot                                   |
| SLACK_CHANNEL        | Notifications go to this channel.  Defaults to `#halo`|
| MONITOR_EVENTS       | Set to `yes` to send critical events to SLACK_CHANNEL |


```
    docker run -d \
        --name don_bot \
        --restart always \
        -e HALO_API_KEY=$HALO_API_KEY \
        -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
        -e SLACK_API_TOKEN=$SLACK_API_TOKEN \
        -e SLACK_CHANNEL=$SLACK_CHANNEL \
        -e MONITOR_EVENTS=$MONITOR_EVENTS \
        docker.io/halotools/don-bot
```

You can add the optional variables, if needed, with:
`-e OPTIONAL_VAR=$OPTIONAL_VAR`

To create a bot user in slack:
* (via Slack) click on Administration -> Manage Apps.
* Search for "bots" in the search box and select the first one.
* Click Add Configuration on the Bot page.
* Choose a username for the bot. "donbot"
* Click on Add bot integration
* The Bot API token will be displayed. 

* Invite donbot to a channel, or message it directly.
* `donbot help` to see available commands.
* Messages picked up by the bot are printed to stdout in the container, which
is useful for understanding how users are interacting with it and how it
interprets messages.


Extending Don-Bot

* `app/donlib/lexicals.py` contains `Lexicals.get_messsage_type()`.
That's where the interpretation and extraction happen.  If you want to
add functionality, that's where you should start.
* There are already some unit tests in `app/test/unit/test_unit_lexicals.py`
to exercise the matching process.  That's a great place to start, and take a
test-driven approach.  Don't even think about offering up a PR for extending
`Lexicals.get_messsage_type()` without having test cases to cover the new work.
Unit testing isn't the highest on this project, but `app/donlib/lexicals.py`
is at 100% and needs to stay that way.

Troubleshooting Don-Bot

* `donbot health` will get you a report of the current availability of all
components.  If `MONITOR_EVENTS` is set to `yes`, you'll also get the timestamp
of the last observed event from the API.
* Don-Bot will periodiaclly self-check and if there's an internal component
failure, it will attempt to drop a message in-channel and exit.  Make sure you
start the container with the `--restart always` argument.
* Failed thread? Use `docker logs CONTAINER_NAME` to ascertain if there's a
stack trace in the bot's logs.
* Not getting the response you expect from interacting with the bot? Have a
look at the test cases for lexicals, found in
`app/test/unit/test_unit_lexicals.py`, to see how your statements align with
 the intended interaction samples in the unit tests.

### Author

Feedback goes to <toolbox@cloudpassage.com>.

### License

See LICENSE.txt


<!---
#CPTAGS:community-supported integration automation
#TBICON:images/python_icon.png
-->
