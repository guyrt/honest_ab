from django.conf.urls import patterns, url

from honest_ab.views import GoalAchievedFormView


urlpatterns = patterns('',
    url(r'^goal/(?P<goal_id>\d+)/$', GoalAchievedFormView.as_view(), name='dashboard_business')
)
