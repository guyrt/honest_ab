from django.http.response import HttpResponse
from django.template.response import SimpleTemplateResponse
from django.test import TestCase
from django.test.client import RequestFactory

from honest_ab.api import get_experiment_bin
from honest_ab.binning_functions.base import CachedExperimentBinningHandlerBase, HONEST_AB_COOKIE_KEY, CachedExperimentDomainChooser
from honest_ab.middleware import HonestABMiddleware
from honest_ab.models import ExperimentDomain, Experiment, ExperimentDomainAllocation


rf = RequestFactory()


class FakeObj(object):

    def __init__(self, pk=42):
        self.pk = pk


class FakeBinningFunction(CachedExperimentBinningHandlerBase):

    def _cookie_key(self, obj, experiment):
        return "fake"

    def _make_decision(self, obj, experiment):
        return "1"


class DomainChooserTestCases(TestCase):

    def setUp(self):
        super(DomainChooserTestCases, self).setUp()
        self.default_domain = ExperimentDomain.objects.get()

    def test_retrieve_cached_domain(self):
        obj = FakeObj(200)
        object_name = '.'.join([str(obj.__class__.__module__), str(obj.__class__.__name__)])
        ExperimentDomainAllocation.objects.create(
            experiment_domain=self.default_domain,
            model=object_name,
            model_pk=200
        )
        experiment = Experiment.objects.create(
            domain=self.default_domain,
            slug="testtest"
        )
        self.assertTrue(CachedExperimentDomainChooser().check_domain(obj, experiment))
        self.assertEqual(1, ExperimentDomainAllocation.objects.count())

    def test_create_new_domain(self):
        # With no assigned domains, create one.
        experiment = Experiment.objects.create(
            domain=self.default_domain,
            slug="testtest"
        )
        self.assertTrue(CachedExperimentDomainChooser().check_domain(FakeObj(100), experiment))
        domain_cache = ExperimentDomainAllocation.objects.get()
        self.assertEqual(domain_cache.model_pk, 100)
        self.assertEqual(domain_cache.experiment_domain, self.default_domain)

    def test_multiple_domains(self):
        # Add second domain (so there will be two)
        # Verify that some tests go to each.
        new_domain = ExperimentDomain.objects.create(
            name="second",
            slug="second"
        )
        experiment = Experiment.objects.create(
            domain=new_domain,
            slug="testtest"
        )

        result_counter = {
            True: 0,
            False: 0
        }
        for i in range(100):
            result_counter[CachedExperimentDomainChooser().check_domain(FakeObj(i * 100), experiment)] += 1
        self.assertGreater(result_counter[True], 30)
        self.assertGreater(result_counter[False], 30)



class ApiTestCases(TestCase):

    def setUp(self):
        super(ApiTestCases, self).setUp()
        self.experiment_domain = ExperimentDomain.objects.create()
        bin_class_string = ".".join([FakeBinningFunction.__module__, FakeBinningFunction.__name__])
        self.experiment = Experiment.objects.create(
            domain=self.experiment_domain,
            decision_class=bin_class_string,
            slug="testtest"
        )

    def test_get_experiment_bin(self):
        group = get_experiment_bin(FakeObj(), self.experiment.slug)
        self.assertEqual(group['honest_ab_experiments']['testtest'], FakeBinningFunction()._make_decision(None, None))

    def test_no_binning_class_found(self):
        pass


class CookieTests(TestCase):
    urls = 'tests.urls'

    def setUp(self):
        super(CookieTests, self).setUp()
        self.experiment_domain = ExperimentDomain.objects.create()
        bin_class_string = ".".join([FakeBinningFunction.__module__, FakeBinningFunction.__name__])
        self.experiment = Experiment.objects.create(
            domain=self.experiment_domain,
            decision_class=bin_class_string,
            slug="testtest"
        )

    def test_sets_cookie_on_use(self):
        # Middleware should set a cookie.
        request = rf.get('test_view/testtest')
        context = {
            'random': 'sample'
        }
        context = get_experiment_bin(FakeObj(), self.experiment.slug, request, context)
        middleware = HonestABMiddleware()
        response = SimpleTemplateResponse(template="", context=context)
        response = middleware.process_response(request, response)

        for key, value in context[HONEST_AB_COOKIE_KEY]['__cache__'].iteritems():
            cookie_value = response.cookies.get(key)
            self.assertIsNotNone(cookie_value)
