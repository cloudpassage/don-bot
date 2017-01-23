import imp
import os
import sys

module_name = 'donlib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
donlib = imp.load_module(module_name, fp, pathname, description)

api_key_id = "APIKEYSAMPLE000"
api_secret_key = "APISECRETKEYSAMPLE000"
api_hostname = "api.nonexist.cloudpassage.com"
api_port = "443"
slack_token = "hello-i-am-a-slack-token"

myname = "donbot"
mymessage = {"text": "donbot hi there"}
mymessages = [mymessage]

dm_sample = {u'text': u'donbot hi', u'ts': u'1485195663.000003',
             u'user': u'U000001D', u'team': u'T3333AM', u'type': u'message',
             u'channel': u'D1R3CT'}

channel_message_sample = {u'text': u'donbot arg', u'ts': u'1485195553.000054',
                          u'user': u'U0000001D', u'team': u'T3AM1D',
                          u'type': u'message', u'channel': u'CHANN31'}

chan_not_found = {u'ok': False, u'error': u'channel_not_found'}

user_sample = {u'ok': True,
               u'user': {u'status': None,
                         u'profile': {u'real_name': u'', u'image_24': u'',
                                      u'real_name_normalized': u'',
                                      u'image_512': u'', u'image_32': u'',
                                      u'image_48': u'', u'image_72': u'',
                                      u'avatar_hash': u'gdb', u'email': u'',
                                      u'image_192': u''},
                         u'tz': None, u'name': u'aaaa', u'deleted': False,
                         u'is_bot': False, u'tz_label':
                         u'Pacific Standard Time', u'real_name': u'',
                         u'color': u'9f69e7', u'team_id': u'T3AM1D',
                         u'is_admin': True, u'is_ultra_restricted': False,
                         u'is_restricted': False, u'is_owner': True,
                         u'tz_offset': -28800, u'id': u'U53R1D',
                         u'is_primary_owner': True}}

user_sample_2 = {u'ok': True,
                 u'user': {u'status': None,
                           u'profile': {u'real_name': u'', u'image_24': u'',
                                        u'real_name_normalized': u'',
                                        u'image_512': u'', u'image_32': u'',
                                        u'image_48': u'', u'image_72': u'',
                                        u'avatar_hash': u'gdb', u'email': u'',
                                        u'image_192': u''},
                           u'tz': None, u'name': u'aaaa', u'deleted': False,
                           u'is_bot': False, u'tz_label':
                           u'Pacific Standard Time', u'real_name': u'',
                           u'color': u'9f69e7', u'team_id': u'T3AM1D',
                           u'is_admin': True, u'is_ultra_restricted': False,
                           u'is_restricted': False, u'is_owner': True,
                           u'tz_offset': -28800, u'id': u'U53RI5N0T',
                           u'is_primary_owner': True}}

chan_sample = {u'ok': True,
               u'channel': {u'topic': {u'last_set': 0, u'value': u'',
                                       u'creator': u''},
                            u'is_general': False, u'name': u'halo',
                            u'is_channel': True, u'created': 1481566604,
                            u'is_member': True, u'is_archived': False,
                            u'creator': u'U53R1D',
                            u'members': [u'U53R1D', u'UB0T'],
                            u'unread_count': 761, u'previous_names': [],
                            u'purpose': {u'last_set': 0, u'value': u'',
                                         u'creator': u''},
                            u'unread_count_display': 681,
                            u'last_read': u'1481566604.000002',
                            u'id': u'CHAN1D',
                            u'latest': {u'text': u'donbot hi',
                                        u'type': u'message',
                                        u'user': u'U53R1D',
                                        u'ts': u'1485196254.000058'}}}


class TestUnitSlack:
    def instantiate_config_helper(self, monkeypatch):
        monkeypatch.setenv('HALO_API_KEY', api_key_id)
        monkeypatch.setenv('HALO_API_SECRET_KEY', api_secret_key)
        monkeypatch.setenv('HALO_API_HOSTNAME', api_hostname)
        monkeypatch.setenv('HALO_API_PORT', api_port)
        monkeypatch.setenv('SLACK_API_TOKEN', slack_token)
        config_obj = donlib.ConfigHelper()
        return config_obj

    def test_unit_slack_init(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        assert donlib.Slack(cfg)

    def test_unit_get_my_messages(self):
        assert donlib.Slack.get_my_messages(myname, mymessages)

    def test_unit_message_is_for_me(self):
        assert donlib.Slack.message_is_for_me(myname, mymessage)

    def test_unit_request_in_safe_chan_true(self):
        assert donlib.Slack.request_in_safe_chan(chan_sample,
                                                 chan_sample)

    def test_unit_request_in_safe_chan_false(self):
        assert not donlib.Slack.request_in_safe_chan(chan_sample,
                                                     chan_not_found)

    def test_unit_requester_is_in_safe_chan(self):
        assert donlib.Slack.requester_is_in_safe_chan(user_sample,
                                                      chan_sample)

    def test_unit_requester_is_in_safe_chan_false(self):
        assert not donlib.Slack.requester_is_in_safe_chan(user_sample_2,
                                                          chan_sample)
