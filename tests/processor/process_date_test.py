from datetime import datetime

import cache_requests
from lxml import html
import predictive_punter
import punters_client
import pymongo
import pytest
import racing_data
import redis
import requests


class CountingProcessor(predictive_punter.Processor):
    """A concrete implementation of Processor that simply counts calls to pre/post_process methods"""

    def __init__(self, *args, **kwargs):

        super(CountingProcessor, self).__init__(*args, **kwargs)

        self.counter = {}

        self.pre_process_date = self.pre_process_meet = self.pre_process_race = self.pre_process_entity
        self.post_process_date = self.post_process_meet = self.post_process_race = self.post_process_entity

    def increment_counter(self, entity, phase):
        """Increment the counter for the entity type"""

        entity_type = entity.__class__

        if entity_type not in self.counter:
            self.counter[entity_type] = {}

        if phase not in self.counter[entity_type]:
            self.counter[entity_type][phase] = 0

        self.counter[entity_type][phase] += 1

    def pre_process_entity(self, entity):
        """Increment the pre phase counter for the specified entity's type"""

        self.increment_counter(entity, 'pre')

    def post_process_entity(self, entity):
        """Increment the post phase counter for the specified entity's type"""

        self.increment_counter(entity, 'post')


@pytest.fixture(scope='module')
def processor():

    database_uri = 'mongodb://localhost:27017/predictive_punter_test'
    database_name = database_uri.split('/')[-1]
    database_client = pymongo.MongoClient(database_uri)
    database_client.drop_database(database_name)
    database = database_client.get_default_database()

    http_client = None
    try:
        http_client = cache_requests.Session(connection=redis.fromurl('redis://localhost:6379/predictive_punter_test'))
    except BaseException:
        try:
            http_client = cache_requests.Session()
        except BaseException:
            http_client = requests.Session()

    html_parser = html.fromstring

    scraper = punters_client.Scraper(http_client, html_parser)

    provider = racing_data.Provider(database, scraper)

    processor = CountingProcessor(provider)
    processor.process_date(datetime(2016, 2, 1))

    return processor


def test_dates(processor):
    """The process_date method should call the pre/post_process_date method the expected number of times"""

    assert processor.counter[datetime]['pre'] == processor.counter[datetime]['post'] == 1


def test_meets(processor):
    """The process_date method should call the pre/post_process_meet method the expected number of times"""

    assert processor.counter[racing_data.Meet]['pre'] == processor.counter[racing_data.Meet]['post'] == 2


def test_races(processor):
    """The process_date method should call the pre/post_process_race method the expected number of times"""

    assert processor.counter[racing_data.Race]['pre'] == processor.counter[racing_data.Race]['post'] == 8 + 8
