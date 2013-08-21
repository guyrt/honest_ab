from django import forms
from honest_ab.binning_functions.base import binning_choices
from honest_ab.models import Experiment


class ExperimentForm(forms.ModelForm):

    decision_class = forms.ChoiceField(choices=binning_choices.choices)

    class Meta:
        model = Experiment
        exclude = ('date_added', 'date_modified')


class GoalAchievedForm(forms.Form):

    model = forms.CharField()
    model_pk = forms.IntegerField()
