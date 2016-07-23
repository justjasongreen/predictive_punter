from datetime import datetime

import pytest
import racing_data


@pytest.fixture(scope='module')
def runner_count():

    return 11 + 14 + 14 + 15 + 10 + 17 + 11 + 15 + 8 + 9 + 11 + 9 + 11 + 10 + 13 + 16


def test_dates(processor, process_date):
    """The process_date method should call the pre/post_process_date method the expected number of times"""

    assert processor.counter[datetime]['pre'] == processor.counter[datetime]['post'] == 1


def test_meets(processor, process_date):
    """The process_date method should call the pre/post_process_meet method the expected number of times"""

    assert processor.counter[racing_data.Meet]['pre'] == processor.counter[racing_data.Meet]['post'] == 2


def test_races(processor, process_date):
    """The process_date method should call the pre/post_process_race method the expected number of times"""

    assert processor.counter[racing_data.Race]['pre'] == processor.counter[racing_data.Race]['post'] == 8 + 8


def test_runners(processor, process_date, runner_count):
    """The process_date method should call the pre/post_process_runner method the expected number of times"""

    assert processor.counter[racing_data.Runner]['pre'] == processor.counter[racing_data.Runner]['post'] == runner_count


def test_horses(processor, process_date, runner_count):
    """The process_date method should call the pre/post_process_horse method the expected number of times"""

    assert processor.counter[racing_data.Horse]['pre'] == processor.counter[racing_data.Horse]['post'] == runner_count


def test_jockeys(processor, process_date, runner_count):
    """The process_date method should call the process_jockey method the expected number of times"""

    assert processor.counter[racing_data.Jockey]['process'] == runner_count


def test_trainers(processor, process_date, runner_count):
    """The process_date method should call the process_trainer method the expected number of times"""

    assert processor.counter[racing_data.Trainer]['process'] == runner_count


def test_performances(processor, process_date):
    """The process_date method should call the process_performance method the expected number of times"""

    assert processor.counter[racing_data.Performance]['process'] > 0
