from django import forms


class GoalAchievedForm(forms.Form):

    model = forms.CharField()
    model_pk = forms.IntegerField()
