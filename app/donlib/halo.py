import cloudpassage
import os
import requests
from formatter import Formatter
from urlparse import urljoin
from utility import Utility as util


class Halo(object):
    """This contains all Halo interaction logic

    Attrubites:
        session (cloudpassage.HaloSession): Halo session object

    """

    def __init__(self, config, health_string, tasks_obj):
        """Initialization only instantiates the session object."""
        self.session = cloudpassage.HaloSession(config.halo_api_key,
                                                config.halo_api_secret_key,
                                                api_host=config.halo_api_host,
                                                api_port=config.halo_api_port,
                                                integration_string=config.ua)
        self.product_version = config.product_version
        self.monitor_events = config.monitor_events
        self.slack_channel = config.slack_channel
        self.health_string = health_string
        self.tasks = tasks_obj
        self.flower_host = config.flower_host
        self.config = config
        return

    def credentials_work(self):
        """Attempts to authenticate against Halo API"""
        good = True
        try:
            self.session.authenticate_client()
        except cloudpassage.CloudPassageAuthentication:
            good = False
        return good

    @classmethod
    def list_tasks_formatted(cls, flower_host):
        """Gets a formatted list of tasks from Flower"""
        report = "Cortex Tasks:\n"
        celery_url = urljoin(flower_host, "api/tasks")
        try:
            response = requests.get(celery_url)
            result = response.json()
        except (ValueError, requests.exceptions.ConnectionError) as e:
            report += "Error: Unable to retrieve task list at this time."
            # We print the output so that it will be retained in the
            # container logs.
            print(e)
            return report
        try:
            for task in result.items():
                    prefmt = {"id": task[0], "name": task[1]["name"],
                              "args": str(task[1]["args"]),
                              "kwargs": str(task[1]["kwargs"]),
                              "started": util.u_to_8601(task[1]["started"]),
                              "tstamp": util.u_to_8601(task[1]["timestamp"]),
                              "state": task[1]["state"],
                              "exception": str(task[1]["exception"])}
                    report += Formatter.format_item(prefmt, "task")
        except AttributeError as e:  # Empty set will throw AttributeError
            print("Halo.list_tasks_formatted(): AttributeError! %s" % e)
            pass
        return report

    def interrogate(self, query_type, target):
        """Entrypoint for report generation

        This method is where you start for generating reports.  When you add
        a new report this is the second place you configure it, right after
        you set it up in Lexicals.get_message_type().

        Returns a finished report, as a string.
        """
        report = "I didn't understand your request. Try asking for help!\n"
        if query_type == "server_report":
            report = self.tasks.report_server_formatted.delay(target)
        elif query_type == "group_report":
            report = self.tasks.report_group_formatted.delay(target)
        elif query_type == "ip_report":
            report = self.get_ip_report(target)
        elif query_type == "all_servers":
            report = self.tasks.list_all_servers_formatted.delay()
        elif query_type == "all_groups":
            report = self.tasks.list_all_groups_formatted.delay()
        elif query_type == "group_firewall_report":
            report = self.tasks.report_group_firewall.delay(target)
        elif query_type == "servers_in_group":
            report = self.tasks.servers_in_group_formatted.delay(target)
        elif query_type == "servers_by_cve":
            report = self.tasks.search_server_by_cve(target)
        elif query_type == "ec2_halo_footprint_csv":
            report = self.tasks.report_ec2_halo_footprint_csv.delay()
        elif query_type == "tasks":
            report = self.list_tasks_formatted(self.flower_host)
        elif query_type == "selfie":
            report = Halo.take_selfie()
        elif query_type == "help":
            report = Halo.help_text()
        elif query_type == "version":
            report = Halo.version_info(self.product_version) + "\n"
        elif query_type == "config":
            report = self.running_config()
        elif query_type == "health":
            report = self.health_string
        return(report)

    @classmethod
    def help_text(cls):
        """This is the help output"""
        ret = ("I currently answer these burning questions, " +
               "but only when you address me by name:\n" +
               "\"tell me about server `(server_id|server_name)`\"\n" +
               "\"tell me about ip `ip_address`\"\n" +
               "\"tell me about group `(group_id|group_name)`\"\n" +
               "\"list all servers\"\n" +
               "\"list server groups\"\n" +
               "\"severs with CVE `cve_id`\"\n" +
               "\"servers in group `(group_id|group_name)`\"\n" +
               "\"group firewall `(group_id|group_name)`\"\n" +
               "\"ec2 halo footprint csv\"\n" +
               "\"version\"\n" +
               "\"tasks\"\n" +
               "\"config\"\n")
        return ret

    @classmethod
    def version_info(cls, product_version):
        return "v%s" % product_version

    def running_config(self):
        if os.getenv("NOSLACK"):
            return "Slack integration is disabled.  CLI access only."
        if self.monitor_events == 'yes':
            events = "Monitoring Halo events"
            conf = ("IP-Blocker Configuration\n" +
                    "------------------------\n" +
                    "IPBLOCKER_ENABLED=%s\n" % (self.config.ipblocker_enable) +
                    "IPBLOCKER_IP_ZONE_NAME=%s\n" % (self.config.ip_zone_name) +  # NOQA
                    "IPBLOCKER_TRIGGER_EVENTS=%s\n" % (self.config.ipblocker_trigger_events) +  # NOQA
                    "IPBLOCKER_TRIGGER_ONLY_ON_CRITICAL=%s\n\n" % (self.config.ipblocker_trigger_only_on_critical) +  # NOQA
                    "Quarantine Configuration\n" +
                    "------------------------\n" +
                    "QUARANTINE_ENABLED=%s\n" % (self.config.quarantine_enable) +  # NOQA
                    "QUARANTINE_TRIGGER_GROUP_NAMES=%s\n" % (self.config.quarantine_trigger_group_names) +  # NOQA
                    "QUARANTINE_TRIGGER_EVENTS=%s\n" % (self.config.quarantine_trigger_events) +  # NOQA
                    "QUARANTINE_TRIGGER_ONLY_ON_CRITICAL=%s\n" % (self.config.quarantine_trigger_only_on_critical) +  # NOQA
                    "QUARANTINE_GROUP_NAME=%s\n\n" % (self.config.quarantine_group_name) +  # NOQA
                    "Event Suppression Configuration\n" +
                    "-------------------------------\n" +
                    "SUPPRESS_EVENTS_IN_CHANNEL=%s\n" % (self.config.suppress_events))  # NOQA
        else:
            events = "NOT monitoring Halo events"
        retval = "%s\nHalo channel: #%s\n%s\n" % (events,
                                                  self.slack_channel,
                                                  conf)
        return retval

    def get_ip_report(self, target):
        """This wraps the report_server_by_id by accepting IP as target"""
        servers = cloudpassage.Server(self.session)
        report = "Unknown IP: \n" + target
        try:
            s_id = servers.list_all(connecting_ip_address=target)[0]["id"]
            report = self.tasks.report_server_formatted(s_id)
        except:
            pass
        return report

    def quarantine_server(self, event):
        server_id = event["server_id"]
        quarantine_group_name = event["quarantine_group"]
        print("Quarantine %s to group %s" % (server_id,
                                             quarantine_group_name))
        return self.tasks.quarantine_server.delay(server_id,
                                                  quarantine_group_name)

    def add_ip_to_blocklist(self, ip_address, block_list_name):
        # We trigger a removal job for one hour out.
        print("Add IP %s to blocklist %s" % (ip_address, block_list_name))
        self.tasks.remove_ip_from_list.apply_async(args=[ip_address,
                                                         block_list_name],
                                                   countdown=3600)
        return self.tasks.add_ip_to_list.delay(ip_address, block_list_name)

    @classmethod
    def take_selfie(cls):
        selfie_file_name = "selfie.txt"
        heredir = os.path.abspath(os.path.dirname(__file__))
        selfie_full_path = os.path.join(heredir, selfie_file_name)
        with open(selfie_full_path, 'r') as s_file:
            selfie = "```" + s_file.read() + "```"
        return selfie
