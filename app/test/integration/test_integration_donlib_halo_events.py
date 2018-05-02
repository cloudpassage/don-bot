import imp
import os
import sys
from dotenv import load_dotenv


here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
config_file = os.path.join(here_dir, "../configuration/local.env")
load_dotenv(dotenv_path=config_file)
sys.path.append(module_path)
# Load donlib
fp, pathname, description = imp.find_module('donlib')
donlib = imp.load_module('donlib', fp, pathname, description)


class TestIntegrationDonlibHaloEvents:
    def instantiate_donlib_config_good(self, monkeypatch):
        monkeypatch.setenv('HALO_API_HOSTNAME', 'api.cloudpassage.com')
        monkeypatch.setenv('HALO_API_PORT', 443)
        monkeypatch.setenv('SLACK_API_TOKEN', 'some_token_')
        config = donlib.ConfigHelper()
        return config

    def test_instantiate_donlib_halo_events(self, monkeypatch):
        """Test instantiation of HaloEvents"""
        config = self.instantiate_donlib_config_good(monkeypatch)
        assert donlib.HaloEvents(config)
