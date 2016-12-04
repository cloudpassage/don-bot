from string import Template as T


class Formatter(object):
    """All the message formatting happens in this class."""
    lib = {"single_server_issue": T("  Issue $rule_key\n" +
                                    "    Status $status\n" +
                                    "    Type     $issue_type\n" +
                                    "    Created  $created_at\n"),
           "single_event": T("  Event $type\n" +
                             "    Critical $critical\n" +
                             "    Created  $created_at\n" +
                             "    Message  $message\n" +
                             "    ----------------------------------------\n"),
           "server_facts": T("---------------------------\n" +
                             "Server Hostname     $hostname\n" +
                             "  Server ID         $id\n" +
                             "  Platform          $platform\n" +
                             "  Platform version  $platform_version\n" +
                             "  OS version        $os_version\n" +
                             "  Group             $group_name\n" +
                             "  Primary IP        $primary_ip_address\n" +
                             "  Connecting IP     $connecting_ip_address\n" +
                             "  State             $state\n" +
                             "  State Change      $last_state_change\n"),
           "policy_meta": T("    Policy name $name\n" +
                            "      Policy type   $poltype \n" +
                            "      Policy ID     $id\n" +
                            "      Description   $description\n" +
                            "      ---------------------------------------\n"),
           "group_facts": T("---------------------------\n" +
                            "Group name $name\n" +
                            "  Group ID      $id\n" +
                            "  Description   $description\n" +
                            "  Tag           $tag\n")}

    @classmethod
    def server_issues(cls, issues):
        """Return list of all issues after sending each through formatter"""
        retval = ""
        for issue in issues:
            retval = retval + Formatter.single_server_issue(issue)
        return retval

    @classmethod
    def group_list(cls, groups):
        """Return list of all servers after sending each through formatter"""
        retval = ""
        for group in groups:
            retval = retval + Formatter.group_facts(group) + "\n"
        return retval

    @classmethod
    def server_list(cls, servers):
        """Return list of all servers after sending each through formatter"""
        if servers == []:
            retval = "No servers in group!"
        else:
            retval = ""
        for server in servers:
            retval = retval + Formatter.server_facts(server) + "\n"
        return retval

    @classmethod
    def single_server_issue(cls, body):
        """Return one issue in friendly text"""
        t = Formatter.lib["single_server_issue"]
        return t.safe_substitute(body)

    @classmethod
    def server_facts(cls, body):
        """Return one server in friendly text"""
        t = Formatter.lib["server_facts"]
        return t.safe_substitute(body)

    @classmethod
    def server_events(cls, events):
        """Return list of all events after sending each through formatter"""
        retval = ""
        for event in events:
            retval = retval + Formatter.single_event(event) + "\n"
        return retval

    @classmethod
    def single_event(cls, body):
        """Return one event in friendly text"""
        t = Formatter.lib["single_event"]
        return t.safe_substitute(body)

    @classmethod
    def policy_meta(cls, body, poltype):
        """Return one policy in friendly text"""
        body["poltype"] = poltype
        t = Formatter.lib["policy_meta"]
        return t.safe_substitute(body)

    @classmethod
    def group_facts(cls, body):
        """Return one group in friendly text"""
        t = Formatter.lib["group_facts"]
        return t.safe_substitute(body)