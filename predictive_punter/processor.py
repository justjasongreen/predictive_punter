import concurrent.futures

from .date_utils import *


class Processor:
    """Abstract class to implement processing of racing entities in a standardised way"""

    def __init__(self, provider, *args, **kwargs):

        self.provider = provider

    @property
    def must_process_meets(self):
        """Return True if this processor instance must process meets or any other associated entities"""

        return hasattr(self, 'pre_process_meet') or hasattr(self, 'post_process_meet') or self.must_process_races

    @property
    def must_process_races(self):
        """Return True if this processor instance must process races or any other associated entities"""

        return hasattr(self, 'pre_process_race') or hasattr(self, 'post_process_race') or self.must_process_runners

    @property
    def must_process_runners(self):
        """Return True if this processor instance must process runners or any other associated entities"""

        return hasattr(self, 'pre_process_runner') or hasattr(self, 'post_process_runner') or self.must_process_horses or self.must_process_jockeys

    @property
    def must_process_horses(self):
        """Return True if this processor instance must process horses"""

        return hasattr(self, 'pre_process_horse') or hasattr(self, 'post_process_horse') or self.must_process_performances

    @property
    def must_process_jockeys(self):
        """Return True if this processor instance must process jockeys"""

        return hasattr(self, 'process_jockey')

    @property
    def must_process_trainers(self):
        """Return True if this processor instance must process trainers"""

        return hasattr(self, 'process_trainer')

    @property
    def must_process_performances(self):
        """Return True if this processor instance must process performances"""

        return hasattr(self, 'process_performance')

    def process_collection(self, collection, target):
        """Asynchronously all items in the specified collection via the specified target"""

        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = [executor.submit(target, item) for item in collection]

            for future in concurrent.futures.as_completed(futures):
                if future.exception() is not None:
                    raise future.exception()

    def process_dates(self, date_from, date_to):
        """Process all dates in the specified range"""

        for date in dates(date_from, date_to):
            self.process_date(date)

    def process_date(self, date):
        """Process the specified date"""

        if hasattr(self, 'pre_process_date'):
            self.pre_process_date(date)

        if self.must_process_meets:
            self.process_collection(self.provider.get_meets_by_date(date), self.process_meet)

        if hasattr(self, 'post_process_date'):
            self.post_process_date(date)

    def process_meet(self, meet):
        """Process the specified meet"""

        if hasattr(self, 'pre_process_meet'):
            self.pre_process_meet(meet)

        if self.must_process_races:
            self.process_collection(meet.races, self.process_race)

        if hasattr(self, 'post_process_meet'):
            self.post_process_meet(meet)

    def process_race(self, race):
        """Process the specified race"""

        if hasattr(self, 'pre_process_race'):
            self.pre_process_race(race)

        if self.must_process_runners:
            self.process_collection(race.runners, self.process_runner)

        if hasattr(self, 'post_process_race'):
            self.post_process_race(race)

    def process_runner(self, runner):
        """Process the specified runner"""

        if hasattr(self, 'pre_process_runner'):
            self.pre_process_runner(runner)

        if self.must_process_horses:
            self.process_horse(runner.horse)

        if self.must_process_jockeys:
            self.process_jockey(runner.jockey)

        if self.must_process_trainers:
            self.process_trainer(runner.trainer)

        if hasattr(self, 'post_process_runner'):
            self.post_process_runner(runner)

    def process_horse(self, horse):
        """Process the specified horse"""

        if hasattr(self, 'pre_process_horse'):
            self.pre_process_horse(horse)

        if self.must_process_performances:
            self.process_collection(horse.performances, self.process_performance)

        if hasattr(self, 'post_process_horse'):
            self.post_process_horse(horse)
