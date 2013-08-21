from django.conf import settings
from django.db.utils import IntegrityError

try:
    HONEST_AB_SKIP_TYPE = settings.HONEST_AB_SKIP_TYPE
except AttributeError:
    HONEST_AB_SKIP_TYPE = 'skip'


class CachedExperimentBinningHandlerBase(object):

    description = "Abstract base class."

    def bin(self, obj, experiment):
        """
        Return the proper bin for an object.

        Use cache if it exists.
        """
        from honest_ab.models import ExperimentAllocation

        object_name = '.'.join([str(obj.__class__.__module__), str(obj.__class__.__name__)])
        import ipdb; ipdb.set_trace()
        try:
            return ExperimentAllocation.objects.get(
                model_pk=obj.pk,
                model=str(obj.__class__),
                experiment=experiment
            ).group
        except ExperimentAllocation.DoesNotExist:
            result = self._make_decision(obj, experiment)
            try:
                ExperimentAllocation.objects.create(
                    experiment=experiment,
                    model=object_name,
                    model_pk=obj.pk,
                    group=result
                )
            except IntegrityError:
                # This can occur in high traffic instances where two threads hit this method
                # at the same time. Both will fail the get and both will try to create.
                return ExperimentAllocation.objects.get(
                    model_pk=obj.pk,
                    model=object_name,
                    experiment=experiment
                ).group
            else:
                return result

    def _make_decision(self, obj, experiment):
        raise NotImplementedError("Your binning handler must decide how to bin users.")


class _BinningClassChoices(object):

    def __init__(self):
        self.choices = []

    def register(self, binning_class):
        """
        Register a binning class with the choices list.

        binning_class should be a subclass (not object) of CachedExperimentBinningHandlerBase.
        description should be something human readable.
        """
        description = binning_class.description
        name = '.'.join([str(binning_class.__module__), binning_class.__name__])
        self.choices.append((name, description))


binning_choices = _BinningClassChoices()
