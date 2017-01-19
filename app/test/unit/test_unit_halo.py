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
api_hostname = "api.cloudpassage.com"
api_port = "443"
slack_token = "hello-i-am-a-slack-token"


with_ec2 = {
      "id": "62061ba0c11",
      "url": "https://api.cloudpassage.com/v1/servers/62061ba0c11",
      "hostname": "ip-10-1-40-209",
      "server_label": None,
      "reported_fqdn": "ip-10-1-40-209.us-west-1.compute.internal",
      "primary_ip_address": None,
      "connecting_ip_address": "54.153.85.184",
      "state": "active",
      "daemon_version": "3.9.3",
      "read_only": False,
      "platform": "redhat",
      "platform_version": "7.3",
      "os_version": "3.10.0-514.el7.x86_64",
      "kernel_name": "Linux",
      "kernel_machine": "x86_64",
      "self_verification_failed": False,
      "connecting_ip_fqdn": "ec2-5-153-85-184.us-west-1.compute.amazonaws.com",
      "last_state_change": "2016-12-13T09:49:04.429Z",
      "group_id": "04b6b400c11911e6972e199079951bd9",
      "group_name": "LINUX",
      "interfaces": [
        {
          "name": "eth0",
          "ip_address": "FE80::413:21FF:FE3C:58C8",
          "netmask": "0.0.0.0"
        },
        {
          "name": "eth0",
          "ip_address": "10.1.40.209",
          "netmask": "255.255.255.0"
        }
      ],
      "aws_ec2": {
        "ec2_instance_id": "i-079f3f5d980613069",
        "ec2_account_id": "856192027328",
        "ec2_kernel_id": None,
        "ec2_image_id": "ami-2cade64c",
        "ec2_availability_zone": "us-west-1b",
        "ec2_region": "us-west-1",
        "ec2_private_ip": "10.1.40.209",
        "ec2_instance_type": "t2.micro",
        "ec2_security_groups": [
          "launch-wizard-121"
        ]
      }
    }

without_ec2 = {
      "id": "1f8fb232c13111e6a10113d2fb",
      "url": "https://api.cloudpassage.com/v1/servers/1f8fb232c13111e6a101",
      "hostname": "WIN-8P86VNPOH0V",
      "server_label": "2012",
      "reported_fqdn": "WIN-8P86VNPOH0V",
      "primary_ip_address": "2001:0:D58:1EF1:34E4:174F:F5FE:D75F",
      "connecting_ip_address": "54.183.221.108",
      "state": "active",
      "daemon_version": "3.9.3",
      "read_only": False,
      "platform": "windows",
      "platform_version": "6.3.9600",
      "os_version": "6.3.9600",
      "kernel_name": "Microsoft Windows Server 2012 R2 Standard",
      "kernel_machine": "64-bit",
      "self_verification_failed": False,
      "connecting_ip_fqdn": "ec2-54-183-221-1.us-west-1.compute.amazonaws.com",
      "last_state_change": "2016-12-13T12:39:00.844Z",
      "group_id": "8f3c54fcc12f11e6972e199079951bd9",
      "group_name": "WIN_test",
      "interfaces": [
        {
          "name": "{C7BAFAFE-DBF4-4C76-B406-8A25283E4CF9}",
          "ip_address": "FE80::FC8D:162B:E9D1:B3D7",
          "netmask": "0.0.0.0",
          "display_name": "Ethernet"
        },
        {
          "name": "{C7BAFAFE-DBF4-4C76-B406-8A25283E4CF9}",
          "ip_address": "10.1.40.160",
          "netmask": "255.255.255.0",
          "display_name": "Ethernet"
        },
        {
          "name": "{FE3C81D3-FB34-40A7-A040-82539BA11902}",
          "ip_address": "FE80::34E4:174F:F5FE:D75F",
          "netmask": "0.0.0.0",
          "display_name": "Local Area Connection* 12"
        },
        {
          "name": "{FE3C81D3-FB34-40A7-A040-82539BA11902}",
          "ip_address": "2001:0:D58:1EF1:34E4:174F:F5FE:D75F",
          "netmask": "0.0.0.0",
          "display_name": "Local Area Connection* 12"
        }
        ]}


class TestUnitHalo:
    def instantiate_config_helper(self, monkeypatch):
        monkeypatch.setenv('HALO_API_KEY', api_key_id)
        monkeypatch.setenv('HALO_API_SECRET_KEY', api_secret_key)
        monkeypatch.setenv('HALO_API_HOSTNAME', api_hostname)
        monkeypatch.setenv('HALO_API_PORT', api_port)
        monkeypatch.setenv('SLACK_API_TOKEN', slack_token)
        config_obj = donlib.ConfigHelper()
        return config_obj

    def test_unit_halo_init(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        assert donlib.Halo(cfg, "")

    def test_unit_help_text(self):
        assert donlib.Halo.help_text()

    def test_unit_selfie(self):
        assert donlib.Halo.take_selfie()

    def test_unit_interrogate_help_text(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        h_obj = donlib.Halo(cfg, "")
        assert h_obj.interrogate("help", "help")

    def test_unit_interrogate_selfie(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        h_obj = donlib.Halo(cfg, "")
        assert h_obj.interrogate("selfie", "selfie")

    def test_unit_credentials_work(self, monkeypatch):
        cfg = self.instantiate_config_helper(monkeypatch)
        h_obj = donlib.Halo(cfg, "")
        assert h_obj.credentials_work() is False

    def test_unit_flatten_ec2(self):
        result = donlib.Halo.flatten_ec2(with_ec2)
        assert result["ec2_region"] == "us-west-1"
        assert result["ec2_security_groups"] == "launch-wizard-121"

    def test_unit_flatten_ec2_no_ec2(self):
        result = donlib.Halo.flatten_ec2(without_ec2)
        assert result["server_label"] == "2012"
