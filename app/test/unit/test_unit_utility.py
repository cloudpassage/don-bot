import imp
import os
import sys

module_name = 'donlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
donlib = imp.load_module(module_name, fp, pathname, description)


class TestUnitUtility:
    def test_utility_8601_today(self):
        assert isinstance(donlib.Utility.iso8601_today(), str)

    def test_unit_utility_8601_yesterday(self):
        assert isinstance(donlib.Utility.iso8601_yesterday(), str)

    def test_unit_utility_8601_one_month_ago(self):
        assert isinstance(donlib.Utility.iso8601_one_month_ago(), str)

    def test_unit_utility_8601_one_week_ago(self):
        assert isinstance(donlib.Utility.iso8601_one_week_ago(), str)

    def test_unit_utility_8601_now(self):
        assert isinstance(donlib.Utility.iso8601_now(), str)

    def test_unit_utility_event_is_critical(self):
        assert donlib.Utility.event_is_critical({"critical": True})

    def test_unit_utility_u_to_8601(self):
        test = 1438049313.073402
        expected = "2015-07-28T02:08:33.073402"
        assert donlib.Utility.u_to_8601(test) == expected
