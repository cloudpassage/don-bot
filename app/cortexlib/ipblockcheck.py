import re


class IpBlockCheck(object):
    def __init__(self, config):
        self.ipblocker_trigger_only_on_critical = config.ipblocker_trigger_only_on_critical  # NOQA
        self.ipblocker_trigger_events = config.ipblocker_trigger_events
        self.ipblocker_enable = config.ipblocker_enable
        self.ip_zone_name = config.ip_zone_name

    def should_block_ip(self, event):
        """Return IP address if IP should be blocked, else return False."""
        if self.ipblocker_enable is False:
            pass
        elif (self.ipblocker_trigger_only_on_critical is True and
                event["critical"] is False):
            pass
        elif event["type"] in self.ipblocker_trigger_events:
            return IpBlockCheck.extract_ip_from_event(event)
        return False

    @classmethod
    def extract_ip_from_event(cls, event):
        """Return IP from Halo event, or return False if IP is not found.

        Add regexes to ``rxen`` list to support more events.
        """
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
        print("Unable to extract IP address from message: %s" %
              event["message"])
        return False
