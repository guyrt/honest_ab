from django.http.response import HttpResponse
from django.template.response import SimpleTemplateResponse
from django.test import TestCase
from django.test.client import RequestFactory

from honest_ab.api import get_experiment_bin
from honest_ab.binning_functions.base import CachedExperimentBinningHandlerBase, HONEST_AB_COOKIE_KEY
from honest_ab.middleware import HonestABMiddleware
from honest_ab.models import ExperimentDomain, Experiment


rf = RequestFactory()


class FakeObj(object):
    pk = 42


class FakeBinningFunction(CachedExperimentBinningHandlerBase):

    def _cookie_key(self, obj, experiment):
        return "fake"

    def _make_decision(self, obj, experiment):
        return "1"


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

    def test_uses_cookie_if_set(self):
        # Set cookie with view then mock call to get data.
        pass
