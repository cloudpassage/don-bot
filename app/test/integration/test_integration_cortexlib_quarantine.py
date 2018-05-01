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


safe_event = {"server_group_name": "NOTME",
              "type": "NOT_A_BAD_TYPE",
              "critical": True}

quar_event = {"critical": True}


class TestIntegrationCortexlibQuarantine:
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

    def instantiate_donlib_config_bad_q_config(self, monkeypatch):
        monkeypatch.setenv('HALO_API_HOSTNAME', 'api.cloudpassage.com')
        monkeypatch.setenv('HALO_API_PORT', 443)
        monkeypatch.setenv('SLACK_API_TOKEN', 'some_token_')
        monkeypatch.setenv('QUARANTINE_TRIGGER_GROUP_NAMES', 'duplicate')
        config = donlib.ConfigHelper()
        return config

    def instantiate_donlib_config_q_disabled(self, monkeypatch):
        monkeypatch.setenv('HALO_API_HOSTNAME', 'api.cloudpassage.com')
        monkeypatch.setenv('HALO_API_PORT', 443)
        monkeypatch.setenv('SLACK_API_TOKEN', 'some_token_')
        monkeypatch.setenv('QUARANTINE_ENABLED', 'false')
        config = donlib.ConfigHelper()
        return config

    def instantiate_cortexlib_quarantine(self, monkeypatch):
        config = self.instantiate_donlib_config_good(monkeypatch)
        q_obj = cortexlib.Quarantine(config)
        return q_obj

    def instantiate_cortexlib_quarantine_bad_conf(self, monkeypatch):
        config = self.instantiate_donlib_config_bad_q_config(monkeypatch)
        q_obj = cortexlib.Quarantine(config)
        return q_obj

    def instantiate_cortexlib_quarantine_bad_keys(self, monkeypatch):
        config = self.instantiate_donlib_config_invalid_halo(monkeypatch)
        q_obj = cortexlib.Quarantine(config)
        return q_obj

    def instantiate_cortexlib_quarantine_disabled(self, monkeypatch):
        config = self.instantiate_donlib_config_q_disabled(monkeypatch)
        q_obj = cortexlib.Quarantine(config)
        return q_obj

    def test_instantiate_cortexlib_quarantine(self, monkeypatch):
        assert self.instantiate_cortexlib_quarantine(monkeypatch)

    def test_trigger_validation_fail_invalid_trigger_group(self, monkeypatch):
        """Walk through scenarios where live validation will fail because of a
        missing group."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        q.quarantine_enable = True
        # Invalid group name causes validation failure
        q.quarantine_trigger_group_names = ["invalidus maximus"]
        q.quarantine_group_name = "donbot testing"
        assert q.config_is_unambiguous() is False

    def test_trigger_validation_fail_ambiguous_quarantine_group(self,
                                                                monkeypatch):
        """Walk through scenario where live validation will fail over duplicate
        groups."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        q.quarantine_enable = True
        # Multiple groups with the same name causes validation failure
        q.quarantine_trigger_group_names = ["duplicate"]
        q.quarantine_group_name = "donbot testing"
        assert q.config_is_unambiguous() is False

    def test_quarantine_event_trigger(self, monkeypatch):
        """Successfully match a quarantine event."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        q_event = quar_event.copy()
        q_event["server_group_name"] = q.quarantine_trigger_group_names[0]
        q_event["type"] = q.quarantine_trigger_events[0]
        q_grp = q.quarantine_group_name
        print(q.quarantine_enable)
        print(q_grp)
        result = q.should_quarantine(q_event)
        print result
        assert result["quarantine_group"] == q_grp

    def test_quarantine_event_crit_no_trigger(self, monkeypatch):
        """Don't trigger quarantine because criticality doesn't pass test."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        q_event = quar_event.copy()
        q_event["server_group_name"] = q.quarantine_trigger_group_names[0]
        q_event["type"] = q.quarantine_trigger_events[0]
        q_event["critical"] = False
        assert q.should_quarantine(q_event) is False

    def test_quarantine_event_no_trigger(self, monkeypatch):
        """This should NOT match as a quarantine event."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        assert q.should_quarantine(safe_event) is False

    def test_quarantine_event_no_trigger_due_to_bad_config(self, monkeypatch):
        """Valid quarantine event should not trigger because config is bad."""
        q = self.instantiate_cortexlib_quarantine_bad_conf(monkeypatch)
        q_event = quar_event.copy()
        q_event["server_group_name"] = q.quarantine_trigger_group_names[0]
        q_event["type"] = q.quarantine_trigger_events[0]
        assert q.should_quarantine(q_event) is False

    def test_quarantine_event_no_trigger_because_disabled(self, monkeypatch):
        """Valid quarantine event should not trigger because Q is disabled."""
        q = self.instantiate_cortexlib_quarantine_disabled(monkeypatch)
        q_event = quar_event.copy()
        q_event["server_group_name"] = q.quarantine_trigger_group_names[0]
        q_event["type"] = q.quarantine_trigger_events[0]
        assert q.should_quarantine(quar_event) is False

    def test_quarantine_event_no_trigger_because_bad_keys(self, monkeypatch):
        """Valid quarantine event should not trigger b/c API keys are bad."""
        q = self.instantiate_cortexlib_quarantine_bad_keys(monkeypatch)
        q_event = quar_event.copy()
        q_event["server_group_name"] = q.quarantine_trigger_group_names[0]
        q_event["type"] = q.quarantine_trigger_events[0]
        assert q.should_quarantine(quar_event) is False

    def test_quarantine_event_no_trigger_bad_group(self, monkeypatch):
        """Quarantine fails because group name does not match."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        q_event = quar_event.copy()
        q_event["server_group_name"] = "Not a target group name"
        q_event["type"] = q.quarantine_trigger_events[0]
        assert q.should_quarantine(q_event) is False

    def test_quarantine_event_no_trigger_no_group(self, monkeypatch):
        """Quarantine fails because group name is missing."""
        q = self.instantiate_cortexlib_quarantine(monkeypatch)
        q_event = quar_event.copy()
        q_event["type"] = q.quarantine_trigger_events[0]
        assert q.should_quarantine(q_event) is False
