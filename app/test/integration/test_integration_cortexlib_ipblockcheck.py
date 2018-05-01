import imp
import os
import sys
from dotenv import load_dotenv


here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
config_file = os.path.join(here_dir, "../configuration/local.env")
load_dotenv(dotenv_path=config_file)
sys.path.append(module_path)
# Load cortexlib
fp, pathname, description = imp.find_module('cortexlib')
cortexlib = imp.load_module('cortexlib', fp, pathname, description)
# Load donlib
fp, pathname, description = imp.find_module('donlib')
donlib = imp.load_module('donlib', fp, pathname, description)

block_event = {"critical": True,
               "message": "Block 192.168.1.1"}


class TestIntegrationCortexlibIPBlockheck:
    def instantiate_donlib_config_good(self, monkeypatch):
        monkeypatch.setenv('HALO_API_HOSTNAME', 'api.cloudpassage.com')
        monkeypatch.setenv('HALO_API_PORT', 443)
        monkeypatch.setenv('SLACK_API_TOKEN', 'some_token_')
        config = donlib.ConfigHelper()
        return config

    def instantiate_donlib_config_invalid_halo(self, monkeypatch):
        monkeypatch.setenv('HALO_API_KEY', 'bad_key')
        monkeypatch.setenv('HALO_API_SECRET_KEY', 'bad_secret')
        monkeypatch.setenv('HALO_API_HOSTNAME', 'api.cloudpassage.com')
        monkeypatch.setenv('HALO_API_PORT', 443)
        monkeypatch.setenv('SLACK_API_TOKEN', 'some_token_')
        config = donlib.ConfigHelper()
        return config

    def instantiate_donlib_config_ibc_disabled(self, monkeypatch):
        monkeypatch.setenv('HALO_API_HOSTNAME', 'api.cloudpassage.com')
        monkeypatch.setenv('HALO_API_PORT', 443)
        monkeypatch.setenv('SLACK_API_TOKEN', 'some_token_')
        monkeypatch.setenv('IPBLOCKER_ENABLED', 'false')
        config = donlib.ConfigHelper()
        return config

    def instantiate_cortexlib_ipblockcheck(self, monkeypatch):
        config = self.instantiate_donlib_config_good(monkeypatch)
        i_obj = cortexlib.IpBlockCheck(config)
        return i_obj

    def test_ipblock_event_trigger(self, monkeypatch):
        """Successfully match ip block event."""
        i = self.instantiate_cortexlib_ipblockcheck(monkeypatch)
        i_event = block_event.copy()
        i_event["type"] = i.ipblocker_trigger_events
        print(i.ipblocker_enable)
        result = i.should_block_ip(i_event)
        print result
        assert result is not False

    def test_ipblock_event_trigger_nocrit(self, monkeypatch):
        """Successfully match ip block event with critical=False."""
        i = self.instantiate_cortexlib_ipblockcheck(monkeypatch)
        i.ipblocker_trigger_only_on_critical = False
        i_event = block_event.copy()
        i_event["type"] = i.ipblocker_trigger_events
        i_event["critical"] = False
        print(i.ipblocker_enable)
        result = i.should_block_ip(i_event)
        print result
        assert result is not False

    def test_ipblock_event_no_trigger_disabled(self, monkeypatch):
        """Don't match because IP blocker is disabled."""
        i = self.instantiate_cortexlib_ipblockcheck(monkeypatch)
        i.ipblocker_enable = False
        i_event = block_event.copy()
        i_event["type"] = i.ipblocker_trigger_events
        print(i.ipblocker_enable)
        result = i.should_block_ip(i_event)
        print result
        assert result is False

    def test_ipblock_event_no_trigger_no_crit(self, monkeypatch):
        """Don't match because event is not critical."""
        i = self.instantiate_cortexlib_ipblockcheck(monkeypatch)
        i.ipblocker_enable = False
        i_event = block_event.copy()
        i_event["type"] = i.ipblocker_trigger_events
        i_event["critical"] = False
        print(i.ipblocker_enable)
        result = i.should_block_ip(i_event)
        print result
        assert result is False

    def test_ipblock_event_no_trigger_no_addy(self, monkeypatch):
        """Don't match because there is not IP in the message."""
        i = self.instantiate_cortexlib_ipblockcheck(monkeypatch)
        i.ipblocker_enable = False
        i_event = block_event.copy()
        i_event["type"] = i.ipblocker_trigger_events
        i_event["critical"] = True
        i_event["message"] = "No IP addy here."
        print(i.ipblocker_enable)
        result = i.should_block_ip(i_event)
        print result
        assert result is False
