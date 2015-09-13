import random
from django.views.generic.base import TemplateView


class FakeObject(object):

    def __init__(self, pk=None):
        self.pk = pk if pk else random.randint(1, 1000000)


class BasicView(TemplateView):

    template_name = 'tested_app/index.html'

    def get_context_data(self, **kwargs):
        """
        Sample context data.
        """
        city_experiment = self.request.honest_ab_resolver['frontend']

        # Use the results to set more context:
        context = dict()
        if city_experiment is None:
            # This means no test was set up.
            context['skip'] = True
        elif city_experiment == 'CityTreatment':
            # Toronto!
            context['baseball'] = 'Blue Jays'
            context['hockey'] = 'Maple Leafs'
            context['basketball'] = 'Raptors'
        elif city_experiment == 'CityControl':
            # Seattle!
            context['baseball'] = 'Mariners'
            context['hockey'] = None
            context['basketball'] = 'Supersonics (well, they were...)'

        return context
