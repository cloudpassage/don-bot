#!/usr/bin/python

import donlib
import sys
import threading
import time
from collections import deque


def main():
    global slack_inbound
    global slack_outbound
    global health_string
    global health_last_event_timestamp
    health_last_event_timestamp = ""
    health_string = ""
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
    print(msg)
    msg = "Don-Bot sends general notifications to #%s" % config.slack_channel
    print(msg)
    if config.monitor_events == "yes":
        print("Starting Halo event monitor")
        halo_collector = threading.Thread(target=event_connector, args=[config])
        halo_collector.daemon = True
        halo_collector.start()

    while True:
        print("Bot Health Report:")
        s_consumer = "  Slack consumer: %s" % str(slack_consumer.is_alive())
        s_emitter = "  Slack emitter: %s" % str(slack_emitter.is_alive())
        h_enricher = "  Halo enricher: %s" % str(halo_enricher.is_alive())
        if config.monitor_events == "yes":
            h_events = "  Halo event monitor: %s" % (halo_collector.is_alive())
        else:
            h_events = ""
        health_string = "\n".join([s_consumer, s_emitter, h_enricher,
                                   h_events, health_last_event_timestamp])
        print(health_string)
        time.sleep(600)


def event_connector(config):
    events = donlib.HaloEvents(config)
    # We add a short delay in case of time drift between container and API
    time.sleep(10)
    while True:
        for event in events:
            health_last_event_timestamp = event["created_at"]
            if donlib.Utility.event_is_critical(event):
                print("Critical event detected!")
                event_fmt = donlib.Formatter.format_item(event, "event")
                slack_outbound.append((config.slack_channel, event_fmt))


def daemon_speaker(config):
    while True:
        halo = donlib.Halo(config, str(health_string))
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

    halo = donlib.Halo(config, "")
    if halo.credentials_work() is False:
        print("Halo credentials are bad!  Exiting!")
        sys.exit(1)

    slack = donlib.Slack(config)
    if slack.credentials_work() is False:
        print("Slack credentials are bad!  Exiting!")
        sys.exit(1)

if __name__ == "__main__":
    main()
