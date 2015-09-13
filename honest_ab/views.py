from django.views.generic.edit import FormView

from honest_ab.api import goal_achieved
from honest_ab.forms import GoalAchievedForm


class GoalAchievedFormView(FormView):
    form_class = GoalAchievedForm()

    def form_valid(self, form):
        goal_achieved(self.kwargs['goal_id'], **form.cleaned_data)
