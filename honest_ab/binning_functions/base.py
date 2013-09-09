import murmur

from django.conf import settings
from django.db.utils import IntegrityError

try:
    HONEST_AB_SKIP_TYPE = settings.HONEST_AB_SKIP_TYPE
except AttributeError:
    HONEST_AB_SKIP_TYPE = 'skip'


try:
    HONEST_AB_COOKIE_KEY = settings.HONEST_AB_COOKIE_KEY
except AttributeError:
    HONEST_AB_COOKIE_KEY = 'honest_ab_experiments'


domain_hash_key = 2130984331297


class CachedExperimentDomainChooser(object):
    """
    Internal domain choice function: randomly assign a given object to a domain.

    Currently, the intention is to not make this a subclassable function. We use
    round robin on the number of domains for choice.
    """

    def check_domain(self, obj, experiment):
        """
        Either get or create assignment.
        """
        from honest_ab.models import ExperimentDomainAllocation
        from honest_ab.models import ExperimentDomain
        try:
            object_name = '.'.join([str(obj.__class__.__module__), str(obj.__class__.__name__)])
            domain_allocation = ExperimentDomainAllocation.objects.get(
                model_pk=obj.pk,
                model=object_name
            )
        except ExperimentDomainAllocation.DoesNotExist:
            num_domains = ExperimentDomain.objects.filter(active=1).count()
            order = murmur.string_hash(str(obj.pk), domain_hash_key) % num_domains
            domain = ExperimentDomain.objects.filter(active=1)[order]
            try:
                ExperimentDomainAllocation.objects.create(
                    experiment_domain=domain,
                    model=object_name,
                    model_pk=obj.pk,
                )
            except IntegrityError:
                # This can occur in high traffic instances where two threads hit this method
                # at the same time. Both will fail the get and both will try to create.
                pass
            return domain.pk == experiment.domain_id
        else:
            return domain_allocation.experiment_domain_id == experiment.domain_id


class CachedExperimentBinningHandlerBase(object):

    description = "Abstract base class."
    cookie_prefix = str(hash("HONEST_AB_"))

    def _get_cookie_cache(self, obj, experiment, request):
        key = CachedExperimentBinningHandlerBase.cookie_prefix + self._cookie_key(obj, experiment)
        return request.get_signed_cookie(key, False, salt=str(experiment.pk))

    def _set_context(self, obj, experiment, context, new_value):
        """
        Add an experiment to the context dict.

        Encapsulate everything in a top level key defined by the module.

        Note that the __cache__ values are only used by the cookie-setting middleware.
        """
        key = CachedExperimentBinningHandlerBase.cookie_prefix + self._cookie_key(obj, experiment)
        if HONEST_AB_COOKIE_KEY not in context:
            context[HONEST_AB_COOKIE_KEY] = dict()
        if '__cache__' not in context[HONEST_AB_COOKIE_KEY]:
            context[HONEST_AB_COOKIE_KEY]['__cache__'] = dict()
        context[HONEST_AB_COOKIE_KEY][experiment.slug] = new_value
        context[HONEST_AB_COOKIE_KEY]['__cache__'][key] = {
            'value': new_value,
            'salt': str(experiment.pk)
        }
        return context

    def bin(self, obj, experiment, request=None, context=None):
        """
        Return an updated context with the appropriate grouping.

        If request is an HttpRequest object, use cookies as cache.
        """
        if context is None:
            context = {}

        if request:
            cookie_cache = self._get_cookie_cache(obj, experiment, request)
            if cookie_cache:
                context = self._set_context(obj, experiment, context, cookie_cache)
                return context

        from honest_ab.models import ExperimentAllocation

        if not CachedExperimentDomainChooser().check_domain(obj, experiment):
            context = self._set_context(obj, experiment, context, HONEST_AB_SKIP_TYPE)
            return context

        object_name = '.'.join([str(obj.__class__.__module__), str(obj.__class__.__name__)])
        try:
            result = ExperimentAllocation.objects.get(
                model_pk=obj.pk,
                model=object_name,
                experiment=experiment
            ).classification
            context = self._set_context(obj, experiment, context, result)
            return context
        except ExperimentAllocation.DoesNotExist:
            result = self._make_decision(obj, experiment)
            try:
                ExperimentAllocation.objects.create(
                    experiment=experiment,
                    model=object_name,
                    model_pk=obj.pk,
                    classification=result
                )
            except IntegrityError:
                # This can occur in high traffic instances where two threads hit this method
                # at the same time. Both will fail the get and both will try to create.
                result = ExperimentAllocation.objects.get(
                    model_pk=obj.pk,
                    model=object_name,
                    experiment=experiment
                ).classification
                context = self._set_context(obj, experiment, context, result)
                return context
            else:
                context = self._set_context(obj, experiment, context, result)
                return context

    def _make_decision(self, obj, experiment):
        raise NotImplementedError("Your binning handler must decide how to bin obj.")

    def _cookie_key(self, obj, experiment):
        raise NotImplementedError("Your binning handler must decide a cookie key.")


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
