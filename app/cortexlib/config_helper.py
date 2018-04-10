import os
import re


class ConfigHelper(object):
    def __init__(self):
        self.ip_zone_name = str(os.getenv("IPBLOCKER_IP_ZONE_NAME"))
        self.ipblocker_enable = self.string_bool(os.getenv("IPBLOCKER_ENABLED"))
        self.ipblocker_trigger_events = self.string_list(os.getenv("IPBLOCKER_TRIGGER_EVENTS"))
        self.ipblocker_trigger_only_on_critical = self.string_bool(os.getenv("IPBLOCKER_TRIGGER_ONLY_ON_CRITICAL"))
        self.quarantine_enable = self.string_bool(os.getenv("QUARANTINE_ENABLED"))
        self.quarantine_trigger_group_names = self.string_list(os.getenv("QUARANTINE_TRIGGER_GROUP_NAME"))
        self.quarantine_trigger_events = self.string_list(os.getenv("QUARANTINE_TRIGGER_EVENTS"))
        self.quarantine_trigger_only_on_critical = self.string_bool(os.getenv("QUARANTINE_TRIGGER_ONLY_ON_CRITICAL"))
        self.quarantine_group_name = str(os.getenv("QUARANTINE_GROUP_NAME"))
        self.validate_config()

    def validate_config(self):
        ref = {
            "quarantine": {
                "enable": [self.quarantine_enable],
                "should_be_lists": [
                    self.quarantine_trigger_group_names,
                    self.quarantine_trigger_events
                ],
                "should_be_bool": [self.quarantine_trigger_only_on_critical],
                "should_be_string": [self.quarantine_group_name]
            },
            "ipblocker": {
                "enable": [self.ipblocker_enable],
                "should_be_lists": [self.ipblocker_trigger_events],
                "should_be_bool": [self.ipblocker_trigger_only_on_critical],
                "should_be_string": [self.ip_zone_name]
            }
        }

        self.validate_type(ref['quarantine']['enable'], bool)
        self.validate_type(ref['ipblocker']['enable'], bool)

        if self.quarantine_enable:
            self.validate_type(ref['quarantine']['should_be_lists'], list)
            self.validate_type(ref['quarantine']['should_be_bool'], bool)
            self.validate_type(ref['quarantine']['should_be_string'], str)

        if self.ipblocker_enable:
            self.validate_type(ref['ipblocker']['should_be_lists'], list)
            self.validate_type(ref['ipblocker']['should_be_bool'], bool)
            self.validate_type(ref['ipblocker']['should_be_string'], str)

    def validate_type(self, obj_lst, var_type):
        for v in obj_lst:
            if not isinstance(v, var_type):
                msg = "%s is not the correct type! Should be a %s" % (str(v), var_type)
                raise ValueError(msg)

    def string_list(self, env_str):
        return env_str.split(",")

    def string_bool(self, env_str):
        if not env_str:
            return None
        if env_str == "True":
            return True
        return False
