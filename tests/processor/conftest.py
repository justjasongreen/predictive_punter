from datetime import datetime

import cache_requests
from lxml import html
import punters_client
import pymongo
import pytest
import racing_data
import redis
import requests

from counting_processor import CountingProcessor


@pytest.fixture(scope='session')
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

    return CountingProcessor(provider)


@pytest.fixture(scope='session')
def process_date(processor):

    processor.reset_counter()
    processor.process_date(datetime(2016, 2, 1))


@pytest.fixture(scope='session')
def process_dates(processor):

    processor.reset_counter()
    processor.process_dates(datetime(2016, 2, 1), datetime(2016, 2, 2))
