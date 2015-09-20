from datetime import datetime
from bisect import bisect_right
from importlib import import_module

from django.conf import settings

from honest_ab.models import Experiment


class ImproperlyConfigured(Exception):
    pass


class HonestABResolver(object):
    """
    Lazy resolver for experiment information

    TODO: use django cache.
    """

    def __init__(self):
        self.load_time = datetime.min
        self.domains = dict()
        self.treatments = dict()
        self.experiment_domain_map = dict()

    def load(self):
        """
        Load all active domains and experiments into memory.
        """
        self.load_time = datetime.now()

        domains = dict()
        treatments = dict()
        experiment_domain_map = dict()
        for experiment in Experiment.objects.select_related('domain').prefetch_related('treatment').filter(active=1):
            experiment_domain = experiment.domain.slug
            experiment_domain_map[experiment.slug] = experiment_domain
            if experiment_domain not in domains:
                domains[experiment_domain] = []
            for bucket_set in experiment.buckets.split(','):
                domains[experiment_domain].extend([(b, experiment.id) for b in bucket_set.split(':')])
            treatments[experiment.id] = [(t.percentage_of_traffic, t.name) for t in experiment.treatments.filter(active=1)]

        self.domains = {k: sorted(v) for k, v in domains}
        self.treatments = treatments
        self.experiment_domain_map = experiment_domain_map

    def __getitem__(self, experiment):
        """
        Look up value of given domain/experiment then:
            - log that we did it.
            - return them.

        todo: accept multiple things here?
        """

        if experiment not in self.experiment_domain_map:
            # TODO - log failure
            return None

        experiment_domain = self.experiment_domain_map[experiment]

        if (datetime.now() - self.load_time).total_seconds() > 60:  # TODO: make setting.
            self.load()

        buckets = self.domains.get(experiment_domain)
        if not buckets:
            return None

        random_bucket = 100

        try:
            idx = find_le(buckets, random_bucket)
            if idx % 2 == 0:
                # is in a group.
                _, experiment_id = buckets[idx]
                # re-randomize user with specific salt.
                pass
            else:
                return None

        except ValueError:
            return None



_resolver = HonestABResolver()


def get_resolver(request):
    """
    Return the in-memory resolver with a request attached.

    TODO: use django cache instead.
    """
    _resolver.request = request
    module_name = '.'.join(settings.HONEST_AB_UNIT_RESOLVER.split('.')[:-1])
    function_name = settings.HONEST_AB_UNIT_RESOLVER.split('.')[-1]
    try:
        ab_unit_resolver_module = import_module(module_name)
    except ValueError:
        raise ImproperlyConfigured("%s isn't an honest_ab experiment resolver module." % module_name)

    try:
        _resolver.id_resolver = getattr(ab_unit_resolver_module, function_name)
    except AttributeError:
        raise ImproperlyConfigured('Honest_ab backend module "%s" does not define a "%s" class.' % (module_name, function_name))

    return _resolver


def find_le(a, x):
    """
    Find rightmost value less than or equal to x.
    Taken with modification from python docs.
    """
    i = bisect_right(a, x)
    if i == len(a) and x != a[-1]:
        raise ValueError
    if i:
        return i - 1
    raise ValueError
