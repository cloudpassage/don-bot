# coding: utf-8
import magic
import mimetypes
import time
from slackclient import SlackClient
from slackclient.server import SlackConnectionError
from socket import error as SocketError
from halocelery.apputils import Utility as hc_util


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
        if self.client.rtm_connect(auto_reconnect=True):
            time.sleep(3)
            ver = str(self.product_version)
            up_msg = u'Don-Bot 👹 v%s started' % ver
            self.client.rtm_send_message(self.channel, up_msg)
        else:
            hc_util.log_stderr("Can't wake up!")
        while True:
            time.sleep(1)
            mymessages = []
            try:
                messages = self.client.rtm_read()
                mymessages = Slack.get_my_messages(self.botname, messages)
            # This covers many common hiccups we see with Slack.
            except SocketError:
                hc_util.log_stderr("Caught SocketError... attempting to reconnect")  # NOQA
                self.client.rtm_connect(auto_reconnect=True)
            # This happens when Slack RTM API has trouble. Wait and retry.
            except SlackConnectionError as e:
                hc_util.log_stderr("Encountered SlackConnectionError: %s" % e)
                time.sleep(5)
                self.client.rtm_connect(auto_reconnect=True)
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

    def send_file(self, channel, report, comment):
        """Slack looks at the file header to determine type"""
        file_ext = self.get_file_extension_for_content(report)
        filename = "Halo_Cortex_Content%s" % file_ext
        hc_util.log_stdout("Uploading %s" % filename)
        self.client.api_call("files.upload",
                             initial_comment=comment,
                             channels=channel,
                             file=report,
                             filename=filename,
                             username=self.botname,
                             icon_url=self.bot_avatar)

    def credentials_work(self):
        good = True
        response = self.client.api_call("auth.test", token=self.token)
        if response["ok"] is not True:
            good = False
        return good

    def get_id_for_channel(self, channel_name):
        all_channels = self.client.api_call("conversations.list", types="public_channel")
        all_groups = self.client.api_call("conversations.list", types="private_channel")
        chan_groups = list(all_channels["channels"])
        chan_groups.extend(all_groups["channels"])
        for channel in chan_groups:
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
        safe_channel_members = self.get_channel_members(safe_channel_id)
        current_channel_id = message["channel"]
        current_channel_info = self.get_channel_info(current_channel_id)
        requester = self.get_user_info(message["user"])
        if Slack.request_in_safe_chan(safe_channel_info, current_channel_info):
            hc_util.log_stdout("Request is in safe channel")
            return True
        elif Slack.requester_is_in_safe_chan(requester, safe_channel_members):
            hc_util.log_stdout("Requester is a member of a safe channel")
            return True
        else:
            hc_util.log_stderr("User is not entitled...\n  %s" % str(message))
            return False

    def get_channel_info(self, channel):
        """Get channel metadata"""

        """deprecated slack api methods"""
        '''ref = {"group": "groups.info",
               "channel": "channels.info"}
        if channel.startswith("G"):
            target = "group"
        elif channel.startswith("D"):
            return self.get_dm_info(channel)
        else:
            target = "channel"
        #return self.client.api_call(ref[target], channel=channel)[target]'''

        return self.client.api_call("conversations.info", channel=channel)

    def get_channel_members(self, channel):
        """Get channel members"""
        return self.client.api_call("conversations.members", channel=channel)

    def get_dm_info(self, channel):
        """deprecated slack api methods"""
        #for x in self.client.api_call("im.list")["ims"]:

        for x in self.client.api_call("conversations.list", types="public_channel,private_channel,mpim,im")["ims"]:
            if x["id"] == channel:
                return x
        return {}

    def get_user_info(self, user):
        """Get user metadata"""
        return self.client.api_call("users.info", user=user)

    @classmethod
    def request_in_safe_chan(cls, safe_chan, current_chan):
        """Compares message's channel ID against the safe channel's ID"""
        result = False
        if safe_chan["channel"]["id"] == current_chan["channel"]["id"]:
            result = True
        return result

    @classmethod
    def requester_is_in_safe_chan(cls, requester, safe_chan):
        """Compares User's ID against safe channel membership"""
        result = False
        if requester["user"]["id"] in safe_chan["members"]:
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

    @classmethod
    def get_file_extension_for_content(cls, content):
        suspect_file_extensions = [".ksh"]
        mime_type = magic.from_buffer(content, mime=True)
        file_ext = mimetypes.guess_extension(mime_type)
        if file_ext in suspect_file_extensions and cls.is_a_csv(content):
            file_ext = ".csv"
        return file_ext

    @classmethod
    def is_a_csv(cls, content):
        well_is_it = True
        lines = content.splitlines()
        if len(lines) == 1:
            well_is_it = False
        else:
            # If every line, split by commas, has the same number of parts,
            # we will call it a CSV.
            field_count = len(lines[0].split(','))
            for line in lines:
                if len(line.split(',')) == field_count:
                    pass
                else:
                    well_is_it = False
        return well_is_it
