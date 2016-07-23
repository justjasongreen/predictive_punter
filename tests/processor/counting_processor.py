import predictive_punter
import racing_data


class CountingProcessor(predictive_punter.Processor):
    """A concrete implementation of Processor that simply counts calls to pre/post_process methods"""

    def __init__(self, *args, **kwargs):

        super(CountingProcessor, self).__init__(*args, **kwargs)

        self.counter = {}

        self.pre_process_date = self.pre_process_meet = self.pre_process_race = self.pre_process_runner = self.pre_process_horse = self.pre_process_entity
        self.post_process_date = self.post_process_meet = self.post_process_race = self.post_process_runner = self.post_process_horse = self.post_process_entity

    def increment_counter(self, entity, phase):
        """Increment the counter for the entity type"""

        entity_type = entity.__class__

        if entity_type not in self.counter:
            self.counter[entity_type] = {}

        if phase not in self.counter[entity_type]:
            self.counter[entity_type][phase] = 0

        self.counter[entity_type][phase] += 1

    def reset_counter(self):
        """Reset the counter to an empty dictionary"""

        self.counter = {}

    def pre_process_entity(self, entity):
        """Increment the pre phase counter for the specified entity's type"""

        self.increment_counter(entity, 'pre')

    def post_process_entity(self, entity):
        """Increment the post phase counter for the specified entity's type"""

        self.increment_counter(entity, 'post')

    def process_jockey(self, jockey):
        """Increment the process phase counter for the Jockey type"""

        self.increment_counter(racing_data.Jockey(self.provider, None) if jockey is None else jockey, 'process')

    def process_trainer(self, trainer):
        """Increment the process phase counter for the Trainer type"""

        self.increment_counter(racing_data.Trainer(self.provider, None) if trainer is None else trainer, 'process')

    def process_performance(self, performance):
        """Increment the process phase counter for the Performance type"""

        self.increment_counter(performance, 'process')
