"""Quarantine functionality is managed here."""
import cloudpassage


class Quarantine(object):
    """Instantiate with a `config` object."""

    def __init__(self, config):
        self.quarantine_enable = config.quarantine_enable
        self.quarantine_group_name = config.quarantine_group_name
        self.quarantine_trigger_group_names = config.quarantine_trigger_group_names  # NOQA
        self.quarantine_trigger_events = config.quarantine_trigger_events
        self.quarantine_trigger_only_on_critical = config.quarantine_trigger_only_on_critical  # NOQA
        self.session = cloudpassage.HaloSession(config.halo_api_key,
                                                config.halo_api_secret_key,
                                                api_host=config.halo_api_host,
                                                api_port=config.halo_api_port,
                                                integration_string=config.ua)

    def should_quarantine(self, event):
        """Return an event object, or False if quarantine should not happen."""
        # If quarantine is not enabled, bail now.
        if self.quarantine_enable is False:
            return False
        event["quarantine_group"] = self.quarantine_group_name
        # If criteria are met and configuration is sane, trigger quarantine.
        if (self.criticality_match(event) is True and
                self.event_type_match(event) is True and
                self.group_name_match(event) is True and
                self.config_is_unambiguous() is True):
            return event
        # Don't trigger by default.
        return False

    def get_all_server_groups(self):
        """Get a list of groups from the Halo API."""
        try:
            server_groups = cloudpassage.ServerGroup(self.session)
            all_groups = server_groups.list_all()
        except cloudpassage.CloudPassageAuthentication:
            print("Quarantine: Authentication failure with CloudPassage API!")
            all_groups = []
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
        if all_groups == []:
            print("Quarantine: Unable to get server groups from Halo! Check your API credentials!")  # NOQA
            return False
        all_configured_groups = []
        all_configured_groups.append(self.quarantine_group_name)
        all_configured_groups.extend(self.quarantine_trigger_group_names[:])
        # Ensure that no more than one group exists per source group name.
        for group in all_configured_groups:
            groups = [x for x in all_groups if x["name"] == group]
            if len(groups) == 0:
                reason += "Quarantine: There is no group named %s\n" % group
                retval = False
            elif len(groups) > 1:
                reason += "Quarantine: More than one group named %s\n" % group
                retval = False
        if retval is False:
            print("Quarantine: Group configuration is ambiguous:\n%s" % reason)
        return retval

    def criticality_match(self, event):
        """Return True if the event's criticality meets requirements."""
        if self.quarantine_trigger_only_on_critical is False:
            return True
        elif (self.quarantine_trigger_only_on_critical is True and
              event["critical"] is True):
            return True
        else:
            print("Quarantine: Event does not meet criticality threshold.")
            return False

    def event_type_match(self, event):
        """Return boolean for event type match."""
        if event["type"] in self.quarantine_trigger_events:
            return True
        else:
            return False

    def group_name_match(self, event):
        """Return bool for server group name match."""
        # If this is not a workload event, return False
        if "server_group_name" not in event:
            return False
        if event["server_group_name"] in self.quarantine_trigger_group_names:
            return True
        else:
            return False
