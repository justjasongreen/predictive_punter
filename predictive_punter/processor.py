class Processor:
    """Abstract class to implement processing of racing entities in a standardised way"""

    @property
    def must_process_dates(self):
        """Return True if this processor instance must process dates"""

        return hasattr(self, 'pre_process_date') or hasattr(self, 'post_process_date')

    def process_date(self, date):
        """Process all racing data for the specified date"""

        if self.must_process_dates:

            if hasattr(self, 'pre_process_date'):
                self.pre_process_date(date)

            if hasattr(self, 'post_process_date'):
                self.post_process_date(date)
