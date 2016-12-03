# Don-Bot

## Halo Slackbot

beta, beta, beta....

Use a read-only CloudPassage Halo API key...

### Running Don-Bot

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
You can add the optional variables in if needed with
`-e OPTIONAL_VAR=$OPTIONAL_VAR`


* Invite donbot to a channel, or message it directly.
* `donbot help` to see available commands.
* Messages picked up by the bot are printed to stdout in the container, which
is useful for understanding how users are interacting with it and how it
interprets messages.


### Extending functionality

* `app/donlib/lexicals.py` contains `Lexicals.get_messsage_type()`.  
That's where the interpretation and extraction happen.  Likely, that'll be
refactored into two functions later on... we'll see...  Anyhow, if you want to
add functionality, that's where you should start.
* There are already some unit tests in `app/test/unit/test_unit_lexicals.py`
to exercise the matching process.  That's a great place to start, and take a
test-driven approach.  Don't even think about offering up a PR for extending
`Lexicals.get_messsage_type()` without having test cases to cover the new work.
Unit testing isn't the highest on this project, but `app/donlib/lexicals.py`
is at 100% and needs to stay that way.
