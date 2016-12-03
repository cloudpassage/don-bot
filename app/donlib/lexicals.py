import re


class Lexicals(object):
    """This contains a number of text parsing methods to derive query logic
    from natural language"""
    @classmethod
    def parse(cls, message):
        """At some point, this should call two methods, one for getting
        the message type, the other for parsing targets from the message"""
        body = message["text"]
        query_type, target = Lexicals.get_message_type(body)
        return(query_type, target)

    @classmethod
    def get_message_type(cls, message):
        retval = ("unknown", "unknown")
        matchers = {r'\sserver\s+(?!group)(?!\")(?P<target>\S+)': "server_report",  # NOQA
                    r'\sserver\s+(?!group)\"(?P<target>[^\"]+)\"': "server_report",  # NOQA
                    r'\s+ip\s+(?P<target>\S+)': "ip_report",
                    r'list\s(all\s)*(?P<target>servers)': "all_servers",
                    r'list\s(all\s)*(?P<target>server\s*groups)': "all_groups",
                    r'(?!\sin)\s+group\s+(?!\")(?P<target>\S+)': "group_report",  # NOQA
                    r'(?!\sin)\s+group\s+\"(?P<target>[^\"]+)\"': "group_report",  # NOQA
                    r'servers\sin\sgroup\s+(?!\")(?P<target>\S+)': "servers_in_group",  # NOQA
                    r'servers\sin\sgroup\s+\"(?P<target>[^\"]+)\"': "servers_in_group",  # NOQA
                    r'(?P<target>selfie)': "selfie",
                    r'(?P<target>help)': "help"}
        for match, name in matchers.items():
            s = re.search(match, message)
            if s:
                retval = (name, s.group('target'))
        print message
        print retval
        return retval
