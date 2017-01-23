import time

from slackclient import SlackClient
from socket import error as SocketError


class Slack(object):
    """This class handles all interaction with Slack.

    Attributes:
        token (str): Slack API token
        client (slackclient.SlackClient): Slack client object

    """

    def __init__(self, config):
        """Instantiation only creates the client attribute"""
        self.token = config.slack_api_token
        self.botname = config.slack_username
        self.bot_avatar = config.slack_icon_url
        self.client = SlackClient(self.token)
        self.channel = config.slack_channel
        self.product_version = config.product_version

    def __iter__(self):
        """This wraps the RTM client, and yields messages"""
        if self.client.rtm_connect():
            time.sleep(1)
            up_msg = "Don-Bot v%s attached to channel" % self.product_version
            self.client.rtm_send_message(self.channel, up_msg)
        else:
            print("Can't wake up!")
        while True:
            time.sleep(1)
            mymessages = []
            try:
                messages = self.client.rtm_read()
                mymessages = Slack.get_my_messages(self.botname, messages)
            except SocketError:
                print("Caught SocketError... attempting to reconnect")
                self.client.rtm_connect()
            if len(mymessages) > 0:
                for message in mymessages:
                    if self.check_request_entitlement(message):
                        yield message
                    else:
                        continue

    def send_message(self, channel, message):
        """For messages under 4k"""
        self.client.api_call("chat.postMessage",
                             channel=channel,
                             text=message,
                             username=self.botname,
                             icon_url=self.bot_avatar)

    def send_report(self, channel, report, comment):
        """For messages > 4k"""
        self.client.api_call("files.upload",
                             initial_comment=comment,
                             channels=channel,
                             content=report,
                             filetype="text",
                             username=self.botname,
                             icon_url=self.bot_avatar)

    def credentials_work(self):
        good = True
        response = self.client.api_call("auth.test", token=self.token)
        if response["ok"] is not True:
            good = False
        return good

    def get_id_for_channel(self, channel_name):
        all_channels = self.client.api_call("channels.list")
        for channel in all_channels["channels"]:
            if channel["name"] == channel_name:
                return channel["id"]
        return None

    def check_request_entitlement(self, message):
        """Checks authorization for requester

        If request is in the configured safe channel (${SLACK_CHANNEL}, or
        #halo by default), we let it through.

        If the requesting user is a member of the safe channel, we let it
        through.
        """
        if "user" not in message:
            return False
        safe_channel_id = self.get_id_for_channel(self.channel)
        safe_channel_info = self.get_channel_info(safe_channel_id)
        current_channel_id = message["channel"]
        current_channel_info = self.get_channel_info(current_channel_id)
        requester = self.get_user_info(message["user"])
        if Slack.request_in_safe_chan(safe_channel_info, current_channel_info):
            print("Request is in safe channel")
            return True
        elif Slack.requester_is_in_safe_chan(requester, safe_channel_info):
            print("Requester is a member of a safe channel")
            return True
        else:
            print("User is not entitled...\n  %s" % str(message))
            return False

    def get_channel_info(self, channel):
        """Get channel metadata"""
        return self.client.api_call("channels.info", channel=channel)

    def get_user_info(self, user):
        """Get user metadata"""
        return self.client.api_call("users.info", user=user)

    @classmethod
    def request_in_safe_chan(cls, safe_chan, current_chan):
        """Compares message's channel ID against the safe channel's ID"""
        result = False
        if current_chan["ok"] is False:  # Channel info !exist if DM
            pass
        elif safe_chan["channel"]["id"] == current_chan["channel"]["id"]:
            result = True
        return result

    @classmethod
    def requester_is_in_safe_chan(cls, requester, safe_chan):
        """Compares User's ID against safe channel mambership"""
        result = False
        if requester["user"]["id"] in safe_chan["channel"]["members"]:
            result = True
        return result

    @classmethod
    def get_my_messages(cls, botname, messages):
        """Returns only messages directed at the bot."""
        mymessages = []
        if not isinstance(messages, list):
            pass
        elif len(messages) == 0:
            pass
        else:
            for message in messages:
                if Slack.message_is_for_me(botname, message):
                    mymessages.append(message)
        return mymessages

    @classmethod
    def message_is_for_me(cls, myname, message):
        is_for_me = False
        if "text" not in message:
            pass
        elif myname in message['text'].lower().split():
            is_for_me = True
        return is_for_me
