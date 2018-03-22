import os
from config_helper import ConfigHelper


class Quarantine(object):
    def __init__(self):
        self.config = ConfigHelper()

    def should_quarantine(self, event):
        """Returns an enriched event object, or False if the event is OK"""
        print self.config
        event["quarantine_group"] = self.config.quarantine_group_name
        if (self.config.quarantine_trigger_only_on_critical is True and
            event["critical"] is False):
            pass
        elif (event["type"] in self.config.quarantine_trigger_events and
              event["server_group_name"] in self.config.quarantine_trigger_group_names):
            return event
        return False



