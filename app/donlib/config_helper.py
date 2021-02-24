import os
import re
from .utility import Utility
from halocelery.apputils import Utility as hc_util


class ConfigHelper(object):
    """This class contains all application configuration variables.

    All configuration variables in this class are derived from environment
    variables.

    Attributes:
        halo_api_key (str): Halo API key, sometimes referred to as 'key id'
        halo_api_secret_key (str): Halo API secret associated with halo_api_key
        halo_api_hostname (str): Hostname for Halo API
        halo_api_port (str): Halo API port
        slack_api_token (str): Slack API token
        slack_username (str): Donbot's user name (purely cosmetic)
        slack_icon (str): Donbot's avatar

    """
    def __init__(self):
        # Halo configs
        self.halo_api_key = os.getenv("HALO_API_KEY", "HARDSTOP")
        self.halo_api_secret_key = os.getenv("HALO_API_SECRET_KEY", "HARDSTOP")
        self.halo_api_host = os.getenv("HALO_API_HOSTNAME", "HARDSTOP")
        self.halo_api_port = os.getenv("HALO_API_PORT", "HARDSTOP")
        self.ua = ConfigHelper.get_ua_string()
        self.product_version = ConfigHelper.get_product_version()
        # Slack configs
        self.slack_api_token = os.getenv("SLACK_API_TOKEN", "HARDSTOP")
        self.slack_username = os.getenv("SLACK_USERNAME", "donbot")
        self.slack_icon_url = os.getenv("SLACK_ICON_URL", "")
        self.slack_channel = os.getenv("SLACK_CHANNEL", "halo")
        # Flower host for task status reporting
        self.flower_host = os.getenv("FLOWER_HOST")
        # IP Blocker configs
        self.ip_zone_name = os.getenv("IPBLOCKER_IP_ZONE_NAME", "")
        self.ipblocker_enable = Utility.bool_from_env("IPBLOCKER_ENABLED")
        self.ipblocker_trigger_events = Utility.list_from_env(
            "IPBLOCKER_TRIGGER_EVENTS")
        self.ipblocker_trigger_only_on_critical = Utility.bool_from_env(
            "IPBLOCKER_TRIGGER_ONLY_ON_CRITICAL")
        # Quarantine configs
        self.quarantine_enable = Utility.bool_from_env("QUARANTINE_ENABLED")
        self.quarantine_trigger_group_names = Utility.list_from_env(
            "QUARANTINE_TRIGGER_GROUP_NAMES")
        self.quarantine_trigger_events = Utility.list_from_env(
            "QUARANTINE_TRIGGER_EVENTS")
        self.quarantine_trigger_only_on_critical = Utility.bool_from_env(
            "QUARANTINE_TRIGGER_ONLY_ON_CRITICAL")
        self.quarantine_group_name = os.getenv("QUARANTINE_GROUP_NAME", "")
        # Event collector configs
        self.monitor_events = os.getenv("MONITOR_EVENTS", "no")
        self.suppress_events = os.getenv("SUPPRESS_EVENTS_IN_CHANNEL", "")
        self.max_threads = 5  # Max threads to be used by event collector
        self.halo_batch_size = 5  # Pagination depth for event collector
        # Check that Quarantine and IP Blocker configs are sane.
        if not self.quarantine_config_is_sane():
            self.quarantine_enable = False
        if not self.ipblocker_config_is_sane():
            self.ipblocker_enable = False

    @classmethod
    def get_ua_string(cls):
        """Return user agent string for Halo API interaction."""
        product = "HaloSlackbot"
        version = ConfigHelper.get_product_version()
        ua_string = product + "/" + version
        return ua_string

    @classmethod
    def get_product_version(cls):
        """Get version of donbot from __init__.py."""
        init = open(os.path.join(os.path.dirname(__file__),
                    "__init__.py")).read()
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        version = rx_compiled.search(init).group(1)
        return version

    def sane(self):
        """Test to make sure that config items for Halo and Slack are set.

        Returns:
            True if everything is OK, False if otherwise

        """
        sanity = True
        template = "Required configuration variable {0} is not set!"
        critical_vars = {"HALO_API_KEY": self.halo_api_key,
                         "HALO_API_SECRET": self.halo_api_secret_key,
                         "HALO_API_HOSTNAME": self.halo_api_host,
                         "HALO_API_PORT": self.halo_api_port,
                         "SLACK_API_TOKEN": self.slack_api_token}
        for name, varval in critical_vars.items():
            if varval == "HARDSTOP":
                sanity = False
                hc_util.log_stdout(template.format(name))
        return sanity

    def quarantine_config_is_sane(self):
        """Sanity check for quarantine configuration."""
        sanity = True
        # Check that trigger group names is a list
        if not isinstance(self.quarantine_trigger_group_names, list):
            hc_util.log_stderr("Quarantine trigger group names\"%s\" failed sanity check." %  # NOQA
                               self.quarantine_trigger_group_names)
            sanity = False
        # Check that trigger events is a list
        if not isinstance(self.quarantine_trigger_events, list):
            hc_util.log_stderr("Quarantine trigger events \"%s\" failed sanity check." %  # NOQA
                               self.quarantine_trigger_events)
            sanity = False
        # Check that quarantine group name is a string
        if not isinstance(self.quarantine_group_name, str):
            hc_util.log_stderr("Quarantine group name \"%s\" failed sanity check." %  # NOQA
                               self.quarantine_group_name)
            sanity = False
        # Check that lists and strings are not zero-length
        for x in [self.quarantine_trigger_events,
                  self.quarantine_trigger_group_names,
                  self.quarantine_group_name]:
            if len(x) == 0:
                hc_util.log_stderr("Quarantine config has empty field(s)")
                sanity = False
        return sanity

    def ipblocker_config_is_sane(self):
        """Sanity check for IP blocker configuration."""
        sanity = True
        # Check that trigger group names is a list
        if not isinstance(self.ip_zone_name, str):
            hc_util.log_stderr("IP Blocker IP zone name failed sanity check.")
            sanity = False
        # Check that trigger events is a list
        if not isinstance(self.ipblocker_trigger_events, list):
            hc_util.log_stderr("IP Blocker trigger events failed sanity check.")  # NOQA
            sanity = False
        # Check that list and string values are not zero-length
        for x in [self.ipblocker_trigger_events,
                  self.ip_zone_name]:
            if len(x) == 0:
                hc_util.log_stderr("IP Blocker config has empty field(s)")
                sanity = False
        return sanity
