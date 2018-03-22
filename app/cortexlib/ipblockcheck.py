import os
import re
from config_helper import ConfigHelper as config


class IpBlockCheck(object):
    def __init__(self):
        return None

    def should_block_ip(self, event):
        if (config.ipblocker_trigger_only_on_critical is True and
            event["critical"] is False):
            pass
        elif event["type"] in config.ipblocker_trigger_events:
            return IpBlockCheck.extract_ip_from_event(event)
        return False

    @classmethod
    def extract_ip_from_event(cls, event):
        rxen = [r'from\s(?P<addy>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\sport',
                r'(?P<addy>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})']
        message = event["message"]
        for rx in rxen:
            m = re.search(rx, message)
            try:
                if m.group("addy"):
                    return m.group("addy")
            except AttributeError:
                pass
        return None
