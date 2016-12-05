import cloudpassage
import os
from formatter import Formatter
from utility import Utility


class Halo(object):
    """This contains all Halo interaction logic

    Attrubites:
        session (cloudpassage.HaloSession): Halo session object

    """

    def __init__(self, config):
        """Initialization only instantiates the session object."""
        self.session = cloudpassage.HaloSession(config.halo_api_key,
                                                config.halo_api_secret_key,
                                                api_host=config.halo_api_host,
                                                api_port=config.halo_api_port)
        return

    def credentials_work(self):
        """Attempts to authenticate against Halo API"""
        good = True
        try:
            self.session.authenticate_client()
        except cloudpassage.CloudPassageAuthentication:
            good = False
        return good

    def interrogate(self, query_type, target):
        """Entrypoint for report generation

        This method is where you start for generating reports.  When you add
        a new report this is the second place you configure it, right after
        you set it up in Lexicals.get_message_type().

        Returns a finished report, as a string.
        """
        report = "What do you even MEAN by saying that?  I just can't even."
        if query_type == "server_report":
            report = self.get_server_report(target)
        elif query_type == "group_report":
            report = self.get_group_report(target)
        elif query_type == "ip_report":
            report = self.get_ip_report(target)
        elif query_type == "all_servers":
            report = self.list_all_servers()
        elif query_type == "all_groups":
            report = self.list_all_groups()
        elif query_type == "servers_in_group":
            report = self.list_servers_in_group(target)
        elif query_type == "selfie":
            report = self.take_selfie()
        elif query_type == "help":
            report = self.help_text()
        return(report)

    def help_text(self):
        """This is the help output"""
        ret = ("I currently answer these burning questions, " +
               "but only when you address me by name:\n " +
               "\"tell me about server `(server_id|server_name)`\"\n" +
               "\"tell me about ip `ip_address`\"\n" +
               "\"tell me about group `(group_id|group_name)`\"\n" +
               "\"list all servers\"\n" +
               "\"list server groups\"\n" +
               "\"servers in group `(group_id|group_name)`\"\n")
        return ret

    def get_group_report(self, target):
        """This is the wrapper method for producing a group report."""
        report = "Group: " + target + "\n"
        group_id = self.get_id_for_group_target(target)
        if group_id is None:
            report = report + "\n is unknown to us..."
            return report
        else:
            try:
                report = report + self.report_group_by_id(group_id)
            except:
                report = report + "\nis unable to be found as id or group name"
        return report

    def get_server_report(self, target):
        """This is the wrapper method for producing a server report."""
        report = "Server: " + target + "\n"
        server_id = self.get_id_for_server_target(target)
        if server_id is None:
            report = report + "\n is unknown to us..."
            return report
        else:
            try:
                report = report + self.report_server_by_id(server_id)
            except cloudpassage.CloudPassageResourceExistence:
                report = report + "\nis unable to be found as id or hostname"
        return report

    def get_id_for_server_target(self, target):
        """Attempts to get server_id using arg:target as hostname, then id"""
        server = cloudpassage.Server(self.session)
        result = server.list_all(hostname=target)
        if len(result) > 0:
            return result[0]["id"]
        else:
            try:
                result = server.describe(target)["id"]
            except:
                result = "Not a hostnamename or server ID: " + target
        return result

    def get_id_for_group_target(self, target):
        """Attempts to get group_id using arg:target as group_name, then id"""
        group = cloudpassage.ServerGroup(self.session)
        orig_result = group.list_all()
        result = []
        for x in orig_result:
            if x["name"] == target:
                result.append(x)
        if len(result) > 0:
            return result[0]["id"]
        else:
            try:
                result = group.describe(target)["id"]
            except cloudpassage.CloudPassageResourceExistence:
                result = "Not a group name or ID (404): " + target
            except KeyError:
                result = "Not a group name or ID (KeyError): " + target
        return result

    def report_server_by_id(self, server_id):
        """Creates a server report from facts and issues"""
        report = self.get_facts(server_id, "server_facts")
        report = report + self.get_server_issues(server_id)
        report = report + self.get_server_events(server_id)
        return report

    def report_group_by_id(self, group_id):
        """Creates a group report"""
        print("Getting group facts")
        report = self.get_facts(group_id, "group_facts")
        print("Getting group policies")
        report = report + self.get_group_policies(group_id)
        return report

    def get_ip_report(self, target):
        """This wraps the report_server_by_id by accepting IP as target"""
        servers = cloudpassage.Server(self.session)
        report = "Unknown IP: " + target
        try:
            s_id = servers.list_all(connecting_ip_address=target)[0]["id"]
            report = self.report_server_by_id(s_id)
        except:
            pass
        return report

    def get_facts(self, obj_id, query_type):
        """Gets facts for servers and groups.

        Args:
            obj_id (str): ID of object to retrieve facts for.

            query_type (str): "server_facts" or "group_facts"

        Returns:
            dict: object facts representation

        """
        if query_type == "server_facts":
            obj_getter = cloudpassage.Server(self.session)
        elif query_type == "group_facts":
            obj_getter = cloudpassage.ServerGroup(self.session)
        else:
            msg = "Unsupported facts query_type: " + query_type
            print(msg)
            return {}
        retval = Formatter.format_item(obj_getter.describe(obj_id), query_type)
        return retval

    def get_group_policies(self, group_id):
        retval = "  Policies\n"
        firewall_keys = ["firewall_policy_id", "windows_firewall_policy_id"]
        csm_keys = ["policy_ids", "windows_policy_ids"]
        fim_keys = ["fim_policy_ids", "windows_fim_policy_ids"]
        group = cloudpassage.ServerGroup(self.session)
        grp_struct = group.describe(group_id)
        print("Getting meta for FW policies")
        for fwp in firewall_keys:
            print(grp_struct[fwp])
            retval = retval + self.get_policy_meta(grp_struct[fwp], "FW")
        print("Getting meta for CSM policies")
        for csm in csm_keys:
            retval = retval + self.get_policy_list(grp_struct[csm], "CSM")
        print("Getting meta for FIM policies")
        for fim in fim_keys:
            retval = retval + self.get_policy_list(grp_struct[fim], "FIM")
        print("Gathered all policy metadata successfully")
        return retval

    def get_policy_list(self, policy_ids, policy_type):
        retval = ""
        for policy_id in policy_ids:
            print(policy_id)
            retval = retval + self.get_policy_meta(policy_id, policy_type)
        return retval

    def list_all_servers(self):
        """Return server list after sending through formatter"""
        server = cloudpassage.Server(self.session)
        report = Formatter.format_list(server.list_all(), "server_facts")
        if report == "":
            report = "No servers in group!"
        return report

    def list_all_groups(self):
        """Return group list after sending through formatter"""
        group = cloudpassage.ServerGroup(self.session)
        report = Formatter.format_list(group.list_all(), "group_facts")
        return report

    def list_servers_in_group(self, target):
        """Return a list of servers in group after sending through formatter"""
        group = cloudpassage.ServerGroup(self.session)
        group_id = self.get_id_for_group_target(target)
        if "Not a group name" in group_id:
            return group_id
        else:
            report = Formatter.format_list(group.list_members(group_id),
                                           "server_facts")
        return report

    def get_server_issues(self, server_id):
        """Return server issues after sending through formatter"""
        pagination_key = 'issues'
        url = '/v2/issues'
        params = {'agent_id': server_id}
        hh = cloudpassage.HttpHelper(self.session)
        report = Formatter.format_list(hh.get_paginated(url,
                                                        pagination_key,
                                                        5,
                                                        params=params),
                                       "issue")
        return report

    def get_server_events(self, server_id):
        """Return server events after sending through formatter"""
        event = cloudpassage.Event(self.session)
        since = Utility.iso8601_today()
        report = Formatter.format_list(event.list_all(10,
                                                      server_id=server_id,
                                                      since=since),
                                       "event")
        return report

    def get_policy_meta(self, policy_id, policy_type):
        p_ref = {"FW": " Firewall",
                 "CSM": "Configuration",
                 "FIM": "File Integrity Monitoring"}
        if policy_id is None:
            return ""
        elif policy_type == "FIM":
            pol = cloudpassage.FimPolicy(self.session)
        elif policy_type == "CSM":
            pol = cloudpassage.ConfigurationPolicy(self.session)
        elif policy_type == "FW":
            pol = cloudpassage.FirewallPolicy(self.session)
        else:
            return ""
        retval = Formatter.policy_meta(pol.describe(policy_id),
                                       p_ref[policy_type])
        return retval

    @classmethod
    def take_selfie(cls):
        selfie_file_name = "selfie.txt"
        heredir = os.path.abspath(os.path.dirname(__file__))
        selfie_full_path = os.path.join(heredir, selfie_file_name)
        with open(selfie_full_path, 'r') as s_file:
            selfie = "```" + s_file.read() + "```"
        return selfie
