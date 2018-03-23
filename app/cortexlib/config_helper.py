import os
import re


class ConfigHelper(object):
    def __init__(self):
        self.ip_zone_name = str(os.getenv("IPBLOCKER_IP_ZONE_NAME"))
        self.ipblocker_enable = self.string_bool("IPBLOCKER_ENABLED")
        self.ipblocker_trigger_events = self.string_list(os.getenv("IPBLOCKER_TRIGGER_EVENTS"))
        self.ipblocker_trigger_only_on_critical = self.string_bool(os.getenv("IPBLOCKER_TRIGGER_ONLY_ON_CRITICAL"))
        self.quarantine_enable = self.string_bool("QUARANTINE_ENABLED")
        self.quarantine_trigger_group_names = self.string_list(os.getenv("QUARANTINE_TRIGGER_GROUP_NAME"))
        self.quarantine_trigger_events = self.string_list(os.getenv("QUARANTINE_TRIGGER_EVENTS"))
        self.quarantine_trigger_only_on_critical = self.string_bool(os.getenv("QUARANTINE_TRIGGER_ONLY_ON_CRITICAL"))
        self.quarantine_group_name = str(os.getenv("QUARANTINE_GROUP_NAME"))
        self.validate_config()

    def validate_config(self):
        ref = {"should_be_lists":  [self.quarantine_trigger_group_names,
                                    self.quarantine_trigger_events,
                                    self.ipblocker_trigger_events],
               "should_be_bool":   [self.quarantine_trigger_only_on_critical,
                                    self.quarantine_enable,
                                    self.ipblocker_trigger_only_on_critical,
                                    self.ipblocker_enable],
               "should_be_string": [self.quarantine_group_name,
                                    self.ip_zone_name]
               }
        for v in ref["should_be_lists"]:
            if not isinstance(v, list):
                msg = "%s is not the correct type!  Should be a list!" % str(v)
                raise ValueError(msg)
        for v in ref["should_be_bool"]:
            if not isinstance(v, bool):
                msg = "%s is not the correct type!  Should be a bool!" % str(v)
                raise ValueError(msg)
        for v in ref["should_be_string"]:
            if not isinstance(v, str):
                msg = "%s is not the correct type!  Should be string!" % str(v)
                raise ValueError(msg)

    def string_list(self, env_str):
        return env_str.split(",")

    def string_bool(self, env_str):
        if not env_str:
            return None
        if env_str == "True":
            return True
        return False