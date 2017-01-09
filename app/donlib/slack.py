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
            attach_message = "Don-Bot v%s attached to channel" % self.product_version
            self.client.rtm_send_message(self.channel, attach_message)
        else:
            print("Can't get WOKE")
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
                    yield message

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
