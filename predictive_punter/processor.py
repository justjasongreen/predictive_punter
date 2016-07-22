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

        return hasattr(self, 'pre_process_runner') or hasattr(self, 'post_process_runner')

    def process_date(self, date):
        """Process the specified date"""

        if hasattr(self, 'pre_process_date'):
            self.pre_process_date(date)

        if self.must_process_meets:
            for meet in self.provider.get_meets_by_date(date):
                self.process_meet(meet)

        if hasattr(self, 'post_process_date'):
            self.post_process_date(date)

    def process_meet(self, meet):
        """Process the specified meet"""

        if hasattr(self, 'pre_process_meet'):
            self.pre_process_meet(meet)

        if self.must_process_races:
            for race in meet.races:
                self.process_race(race)

        if hasattr(self, 'post_process_meet'):
            self.post_process_meet(meet)

    def process_race(self, race):
        """Process the specified race"""

        if hasattr(self, 'pre_process_race'):
            self.pre_process_race(race)

        if self.must_process_runners:
            for runner in self.provider.get_runners_by_race(race):  # TODO: race.runners
                self.process_runner(runner)

        if hasattr(self, 'post_process_race'):
            self.post_process_race(race)

    def process_runner(self, runner):
        """Process the specified runner"""

        if hasattr(self, 'pre_process_runner'):
            self.pre_process_runner(runner)

        if hasattr(self, 'post_process_runner'):
            self.post_process_runner(runner)
