#!/usr/bin/python

import donlib
import sys
import threading
import time
from collections import deque
from multiprocessing import Pool


def main():
    global slack_inbound
    global slack_outbound
    slack_inbound = deque([])
    slack_outbound = deque([])
    config = donlib.ConfigHelper()
    """First we make sure that all configs are sound..."""
    check_configs(config)
    """Next, we start the Slack ingestion thread..."""
    slack_consumer = threading.Thread(target=slack_in_manager, args=[config])
    slack_consumer.daemon = True
    slack_consumer.start()
    """Now, we start the Slack emitter..."""
    slack_emitter = threading.Thread(target=slack_out_manager, args=[config])
    slack_emitter.daemon = True
    slack_emitter.start()
    """Finally, we start up the Daemon Speaker"""
    halo_enricher = threading.Thread(target=daemon_speaker, args=[config])
    halo_enricher.daemon = True
    halo_enricher.start()
    msg = "Starting Don-Bot v%s\nName is set to %s" % (donlib.__version__,
                                                       config.slack_username)
    print msg

    while True:
        time.sleep(60)


def daemon_speaker(config):
    while True:
        halo = donlib.Halo(config)
        try:
            message = slack_inbound.popleft()
            channel = message["channel"]
            halo_query, target = donlib.Lexicals.parse(message)
            halo_results = halo.interrogate(halo_query, target)
            slack_outbound.append((channel, halo_results))
        except IndexError:
            time.sleep(1)
    return


def slack_in_manager(config):
    slack = donlib.Slack(config)
    for message in slack:
        print("Message in slack consumer")
        slack_inbound.append(message)


def slack_out_manager(config):
    slack = donlib.Slack(config)
    while True:
        try:
            message = slack_outbound.popleft()
            if len(message[1]) > 4000:
                slack.send_report(message[0], message[1], "Daemonic Report")
            else:
                slack.send_message(message[0], message[1])
        except IndexError:
            time.sleep(1)


def check_configs(config):
    if config.sane() is False:
        print("Configuration is bad!  Exiting!")
        sys.exit(1)

    halo = donlib.Halo(config)
    if halo.credentials_work() is False:
        print("Halo credentials are bad!  Exiting!")
        sys.exit(1)

    slack = donlib.Slack(config)
    if slack.credentials_work() is False:
        print("Slack credentials are bad!  Exiting!")
        sys.exit(1)

if __name__ == "__main__":
    main()
