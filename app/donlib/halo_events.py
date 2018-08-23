"""This class provides an iterator.  Under the covers it does multi-threaded
consumption of events, only providing information to the iterator when it's
been ordered correctly."""

import cloudpassage
from halocelery.apputils import Utility as hc_util


class HaloEvents(object):
    """Instantiate with a donlib.ConfigHelper() object as an argument."""
    def __init__(self, config):
        self.halo_key = config.halo_api_key
        self.halo_secret = config.halo_api_secret_key
        self.halo_api_host = config.halo_api_host
        self.halo_api_port = config.halo_api_port
        self.ua = config.ua
        self.start_timestamp = self.starting_event_time()
        hc_util.log_stdout("Event Collector: Starting timestamp: " + self.start_timestamp)  # NOQA

    def __iter__(self):
        """This allows us to iterate through the events stream."""
        session = self.build_halo_session()
        streamer = cloudpassage.TimeSeries(session, self.start_timestamp,
                                           "/v1/events", "events")
        while True:
            try:
                for event in streamer:
                    yield event
            except IndexError:
                pass

    def starting_event_time(self):
        session = self.build_halo_session()
        api = cloudpassage.HttpHelper(session)
        url = "/v1/events?sort_by=created_at.desc&per_page=1"
        resp = api.get(url)
        return resp['events'][0]['created_at']

    def build_halo_session(self):
        """This creates the halo session object for API interaction."""
        session = cloudpassage.HaloSession(self.halo_key, self.halo_secret,
                                           api_host=self.halo_api_host,
                                           api_port=self.halo_api_port,
                                           integration_string=self.ua)
        return session
