class Processor:
    """Abstract class to implement processing of racing entities in a standardised way"""

    def __init__(self, provider, *args, **kwargs):

        self.provider = provider

    @property
    def must_process_meets(self):
        """Return True if this processor instance must process meets or any other associated entities"""

        return hasattr(self, 'pre_process_meet') or hasattr(self, 'post_process_meet')

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

        if hasattr(self, 'post_process_meet'):
            self.post_process_meet(meet)