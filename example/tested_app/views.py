import random
from django.views.generic.base import TemplateView
from honest_ab.api import get_experiment_bin
from honest_ab.binning_functions.base import HONEST_AB_COOKIE_KEY, HONEST_AB_SKIP_TYPE


class FakeObject(object):

    def __init__(self, pk=None):
        self.pk = pk if pk else random.randint(1, 1000000)


class BasicView(TemplateView):

    template_name = 'tested_app/index.html'

    def get_context_data(self, **kwargs):
        """
        Sample context data.
        """
        context = get_experiment_bin(FakeObject(), 'city', self.request)

        # Use the results to set more context:
        if context[HONEST_AB_COOKIE_KEY]['city'] == HONEST_AB_SKIP_TYPE:
            # This means no test was set up.
            context['skip'] = True
        elif context[HONEST_AB_COOKIE_KEY]['city'] == '0':
            # Toronto!
            context['baseball'] = 'Blue Jays'
            context['hockey'] = 'Maple Leafs'
            context['basketball'] = 'Raptors'
        elif context[HONEST_AB_COOKIE_KEY]['city'] == '1':
            # Seattle!
            context['baseball'] = 'Mariners'
            context['hockey'] = None
            context['basketball'] = 'Supersonics (well, they were...)'

        return context
