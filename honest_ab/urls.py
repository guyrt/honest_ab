from django.conf.urls import patterns, url

from honest_ab.views import GoalAchievedView, GoalAchievedFormView


urlpatterns = patterns('',
    url(r'^goal/(?P<goal_id>\d+)/(?P<experiment_allocation_id>)$', GoalAchievedView.as_view(), name='dashboard_business'),
    url(r'^goal/(?P<goal_id>\d+)/$', GoalAchievedFormView.as_view(), name='dashboard_business')
)
