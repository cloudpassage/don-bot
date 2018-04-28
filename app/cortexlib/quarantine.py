"""Quarantine functionality is managed here."""
import cloudpassage


class Quarantine(object):
    """Instantiate with a `config` object."""

    def __init__(self, config):
        self.config = config
        self.session = cloudpassage.HaloSession(config.halo_api_key,
                                                config.halo_api_secret_key,
                                                api_host=config.halo_api_host,
                                                api_port=config.halo_api_port,
                                                integration_string=config.ua)

    def should_quarantine(self, event):
        """Return an event object, or False if quarantine should not happen."""
        # If quarantine is not enabled, bail now.
        if self.config.quarantine_enable is False:
            return False
        event["quarantine_group"] = self.config.quarantine_group_name
        # If criteria are met and configuration is sane, trigger quarantine.
        if (self.criticality_match is True and
                self.event_type_match is True and
                self.config_is_unambiguous is True):
            return event
        else:
            pass
        # Don't trigger by default.
        return False

    def get_all_server_groups(self):
        """Get a list of groups from the Halo API."""
        server_groups = cloudpassage.ServerGroup(self.session)
        all_groups = server_groups.list_all()
        return all_groups

    def config_is_unambiguous(self):
        """Ensure that configuration is unambiguous.

        Every goup named in quarantine config must have exactly one
        match in the Halo account.  If more than one exists, bail because
        of ambiguous configuration.
        """
        retval = True
        reason = ""
        all_groups = self.get_all_server_groups()
        quar_group = self.config.quarantine_group_name
        src_groups = self.config.quarantine_trigger_group_names
        all_configured_groups = quar_group.extend(src_groups)
        # Ensure that no more than one group exists per source group name.
        for group in all_configured_groups:
            groups = [x for x in all_groups if x["name"] == group]
            if len(groups) == 0:
                reason += "There is no group named %s\n" % group
                retval = False
            elif len(groups) > 1:
                reason += "More than one group named %s\n" % group
                retval = False
            else:
                continue
        if retval is False:
            print("Quarantine group configuration is ambiguous:\n%s" % reason)
        return retval

    def criticality_match(self, event):
        """Return True if the event's criticality meets requirements."""
        if self.config.quarantine_trigger_only_on_critical is False:
            return True
        elif (self.config.quarantine_trigger_only_on_critical is True and
              event["critical"] is True):
            return True
        else:
            return False

    def event_type_match(self, event):
        """Return boolean for event type match."""
        if event["type"] in self.config.quarantine_trigger_events:
            return True
        else:
            return False
