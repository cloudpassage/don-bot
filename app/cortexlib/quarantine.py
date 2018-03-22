import os


class Quarantine(object):
    def __init__(self):
        self.trigger_group_names = []
        self.quarantine_group_name = ""
        self.trigger_events = []
        self.trigger_only_on_critical = True
        self.set_quarantine_config()
        self.validate_config()

    def should_quarantine(self, event):
        """Returns an enriched event object, or False if the event is OK"""
        event["quarantine_group"] = self.quarantine_group_name
        if (self.trigger_only_on_critical is True and
            event["critical"] is False):
            pass
        elif (event["type"] in self.trigger_events and
              event["server_group_name"] in self.trigger_group_names):
            return event
        return False

    def set_quarantine_config(self):
        self.trigger_group_names = self.string_list(os.getenv("QUARANTINE_TRIGGER_GROUP_NAME"))
        self.trigger_events = self.string_list(os.getenv("QUARANTINE_TRIGGER_EVENTS"))
        self.trigger_only_on_critical = self.string_bool(os.getenv("QUARANTINE_TRIGGER_ONLY_ON_CRITICAL"))
        self.quarantine_group_name = str(os.getenv("QUARANTINE_GROUP_NAME"))

    def validate_config(self):
        ref = {"should_be_lists": [self.trigger_group_names,
                                   self.trigger_events],
               "should_be_bool": [self.trigger_only_on_critical],
               "should_be_string": [self.quarantine_group_name]}
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
