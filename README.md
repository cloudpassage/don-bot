# Don-Bot, the Halo Slackbot

[![Build Status](https://travis-ci.org/ashmastaflash/don-bot.svg?branch=master)](https://travis-ci.org/ashmastaflash/don-bot)
[![Code Climate](https://codeclimate.com/github/ashmastaflash/don-bot/badges/gpa.svg)](https://codeclimate.com/github/ashmastaflash/don-bot)
[![Issue Count](https://codeclimate.com/github/ashmastaflash/don-bot/badges/issue_count.svg)](https://codeclimate.com/github/ashmastaflash/don-bot)
[![Test Coverage](https://codeclimate.com/github/ashmastaflash/don-bot/badges/coverage.svg)](https://codeclimate.com/github/ashmastaflash/don-bot/coverage)


## Summary

This is a chatbot that allows you to query your CloudPassage Halo account
without leaving the comfort of your Slack client.  No need to log into the
web portal to find out the status of a server- just
`donbot tell me about server XYZ`.

It lives in a Docker container, so you can deploy pretty much anywhere.  
No listening ports, it just establishes a connection to Slack and listens
for messages where it's name is mentioned. Then it reaches out to the
CloudPassage Halo API to gather information, and drops a report back into the
channel where it was requested.


Use a read-only CloudPassage Halo API key...

### Running Don-Bot

Requirements:

* CloudPassage Halo READ-ONLY API key
* Slack chatbot token

Doing the thing:

1. Clone it `git clone https://github.com/ashmastaflash/don-bot`
1. Descend into the repo root `cd don-bot`
1. Build the container `docker build -t don-bot .`
1. Set the following env vars, and then run:

| var                 | purpose                                      |
|---------------------|----------------------------------------------|
| HALO_API_KEY        | Halo API key ID                              |
| HALO_API_SECRET_KEY | Halo API secret                              |
| HALO_API_HOSTNAME   | OPTIONAL- defaults to api.cloudpassage.com   |
| HALO_API_PORT       | OPTIONAL- defaults to 443                    |
| SLACK_API_TOKEN     | Slack token for bot                          |
| SLACK_USERNAME      | OPTIONAL- defaults to `donbot`               |
| SLACK_ICON_URL      | OPTIONAL- Link to avatar image for bot       |

```
    docker run -it --rm \
        -e HALO_API_KEY=$HALO_API_KEY \
        -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
        -e SLACK_API_TOKEN=$SLACK_API_TOKEN \
        don-bot
```

You can add the optional variables, if needed, with:
`-e OPTIONAL_VAR=$OPTIONAL_VAR`


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

### Author

This tool was written by Ash Wilson (@ashmastaflash).  Feedback should go to
<toolbox@cloudpassage.com>.

### License

See LICENSE.txt
