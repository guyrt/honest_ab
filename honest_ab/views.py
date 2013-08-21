from django.http.response import HttpResponse, Http404
from django.views.generic import View
from django.views.generic.edit import FormView

from honest_ab.api import goal_achieved
from honest_ab.forms import GoalAchievedForm
from honest_ab.models import ExperimentAllocation, Goal


class GoalAchievedView(View):

    def post(self, *args, **kwargs):
        if ExperimentAllocation.objects.filter(id=self.kwargs['experiment_allocation_id']).exists() \
                and Goal.objects.filter(id=self.kwargs['goal_id']).exists():

            goal_achieved(experiment_allocation_id=self.kwargs['experiment_allocation_id'], goal=self.kwargs['goal_id'])
            return HttpResponse()
        else:
            raise Http404()


class GoalAchievedFormView(FormView):
    form_class = GoalAchievedForm()

    def form_valid(self, form):
        goal_achieved(self.kwargs['goal_id'], **form.cleaned_data)

