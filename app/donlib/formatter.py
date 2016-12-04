from string import Template as T


class Formatter(object):
    """All the message formatting happens in this class."""
    lib = {"issue": T("  Issue $rule_key\n" +
                      "    Status $status\n" +
                      "    Type     $issue_type\n" +
                      "    Created  $created_at\n"),
           "event": T("  Event $type\n" +
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
    def format_list(cls, items, item_type):
        retval = ""
        for item in items:
            retval = retval + Formatter.format_item(item, item_type)
        return retval

    @classmethod
    def format_item(cls, item, item_type):
        t = Formatter.lib[item_type]
        retval = t.safe_substitute(item)
        return retval

    @classmethod
    def policy_meta(cls, body, poltype):
        """Return one policy in friendly text"""
        body["poltype"] = poltype
        t = Formatter.lib["policy_meta"]
        return t.safe_substitute(body)
