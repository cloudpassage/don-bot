import os


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
        self.halo_api_key = os.getenv("HALO_API_KEY", "HARDSTOP")
        self.halo_api_secret_key = os.getenv("HALO_API_SECRET_KEY", "HARDSTOP")
        self.halo_api_host = os.getenv("HALO_API_HOSTNAME", "HARDSTOP")
        self.halo_api_port = os.getenv("HALO_API_PORT", "HARDSTOP")
        self.slack_api_token = os.getenv("SLACK_API_TOKEN", "HARDSTOP")
        self.slack_username = os.getenv("SLACK_USERNAME", "donbot")
        self.slack_icon_url = os.getenv("SLACK_ICON_URL", "")

    def sane(self):
        """Tests to make sure that required config items are set.

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
                print(template.format(name))
        return sanity
