import imp
import os
import pytest
import sys
from dotenv import load_dotenv


module_name = 'cortexlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
config_file = os.path.join(here_dir, "../configuration/local.env")
load_dotenv(dotenv_path=config_file)
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cortexlib = imp.load_module(module_name, fp, pathname, description)


safe_event = {"server_group_name": "NOTME",
              "type": "NOT_A_BAD_TYPE",
              "critical": True}

quar_event = {"critical": True}


class TestIntegrationCortexlibQuarantine:
    def instantiate_cortexlib_quarantine(self):
        q_obj = cortexlib.Quarantine()
        return q_obj

    def test_instantiate_cortexlib_quarantine(self):
        assert self.instantiate_cortexlib_quarantine()

    def test_trigger_validation_fail(self):
        q = self.instantiate_cortexlib_quarantine()
        q.config.quarantine_enable = True
        with pytest.raises(ValueError):
            q.config.quarantine_trigger_events = 123
            q.config.validate_config()
        with pytest.raises(ValueError):
            q.config.quarantine_trigger_group_names = "invalidus maximus"
            q.config.validate_config()
        with pytest.raises(ValueError):
            q.config.quarantine_quarantine_group_name = ["invalidus minimus"]
            q.config.validate_config()
        with pytest.raises(ValueError):
            q.config.quarantine_trigger_only_on_critical = "YAS"
            q.config.validate_config()

    def test_quarantine_event_trigger(self):
        q = self.instantiate_cortexlib_quarantine()
        quar_event["server_group_name"] = q.config.quarantine_trigger_group_names[0]
        quar_event["type"] = q.config.quarantine_trigger_events[0]
        q_grp = q.config.quarantine_group_name
        assert q.should_quarantine(quar_event)["quarantine_group"] == q_grp

    def test_quarantine_event_no_trigger(self):
        q = self.instantiate_cortexlib_quarantine()
        assert q.should_quarantine(safe_event) is False
