import murmur
import random

from honest_ab.models import ExperimentAllocation
from honest_ab.binning_functions.base import CachedExperimentBinningHandlerBase, binning_choices, HONEST_AB_SKIP_TYPE


class CachedExperimentDefaultBinner(CachedExperimentBinningHandlerBase):

    description = "Default binning algorithm: Hash model pk and take modulus by number of classes."

    def _make_decision(self, obj, experiment):
        """
        Use a simple hash on the string value of the object pk.
        """
        if random.random() * 100 > experiment.percentage_of_traffic:
            result = HONEST_AB_SKIP_TYPE
        else:
            result = str(murmur.string_hash(str(obj.pk), experiment.pk) % experiment.number_of_classes)

        return result


binning_choices.register(CachedExperimentDefaultBinner)
