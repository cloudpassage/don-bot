"""This class provides an iterator.  Under the covers it does multi-threaded
consumption of events, only providing information to the iterator when it's
been ordered correctly."""

import cloudpassage
import operator
import time
import urllib
import utility
from multiprocessing.dummy import Pool as ThreadPool


class HaloEvents(object):

    def __init__(self, config):
        self.halo_key = config.halo_api_key
        self.halo_secret = config.halo_api_secret_key
        self.start_timestamp = utility.Utility.iso8601_now()
        self.max_threads = config.max_threads
        self.halo_batch_size = config.halo_batch_size
        self.last_event_timestamp = None
        self.events = []
        self.halo_session = None
        self.last_event_id = ""
        self.ua = config.ua

    def __iter__(self):
        while True:
            print "Last event timestamp: %s" % str(self.last_event_timestamp)
            try:
                for event in self.get_next_batch():
                    yield event
            except IndexError:
                time.sleep(5)

    def get_next_batch(self):
        url_list = self.create_url_list()
        try:
            pages = self.get_pages(url_list)
        except ConnectionError:  # Sometimes connection abort happens
            pages = [{"events": []}]
        events = self.events_from_pages(pages)
        if events[0]["id"] == self.last_event_id:
            del events[0]
        try:
            last_event_timestamp = events[-1]['created_at']
            last_event_id = events[-1]['id']
            self.last_event_id = last_event_id
            self.last_event_timestamp = last_event_timestamp
        except IndexError:
            pass
        return events

    def events_from_pages(self, pages):
        events = []
        for page in pages:
            for event in page["events"]:
                events.append(event)
        result = self.order_events(events, "created_at")
        return result

    def order_events(self, events, sort_key):
        sorted_list = sorted(events, key=operator.itemgetter(sort_key))
        return sorted_list

    def build_halo_session(self):
        halo_session = cloudpassage.HaloSession(self.halo_key,
                                                self.halo_secret,
                                                integration_string=self.ua)
        return halo_session

    def create_url_list(self):
        """We initially set the 'since' var to the start_timestamp.  The next
        statement will override that value with the last event's timestamp, if
        one is set

        """

        base_url = "/v1/events"
        modifiers = {}
        url_list = []
        if self.start_timestamp is not None:
            modifiers["since"] = self.start_timestamp
        if self.last_event_timestamp is not None:
            modifiers["since"] = self.last_event_timestamp
        for page in range(1, self.halo_batch_size + 1):
            url = None
            modifiers["page"] = page
            url = self.build_url(base_url, modifiers)
            url_list.append(url)
        return url_list

    @classmethod
    def build_url(cls, base_url, modifiers):
        params = urllib.urlencode(modifiers)
        url = "%s?%s" % (base_url, params)
        return url

    def get_pages(self, url_list):
        halo_session = self.build_halo_session()
        page_helper = cloudpassage.HttpHelper(halo_session)
        pool = ThreadPool(self.max_threads)
        results = pool.map(page_helper.get, url_list)
        pool.close()
        pool.join()
        return results
