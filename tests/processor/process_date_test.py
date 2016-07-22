from datetime import datetime

import predictive_punter


class CountingProcessor(predictive_punter.Processor):
    """A concrete implementation of Processor that simply counts calls to pre/post_process methods"""

    def __init__(self, *args, **kwargs):

        super(CountingProcessor, self).__init__(*args, **kwargs)

        self.counter = {}

        self.pre_process_date = self.pre_process_entity
        self.post_process_date = self.post_process_entity

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


def test_dates():
    """The process_date method should call the pre/post_process_date method the expected number of times"""

    processor = CountingProcessor()
    processor.process_date(datetime(2016, 2, 1))

    assert processor.counter[datetime]['pre'] == processor.counter[datetime]['post'] == 1
