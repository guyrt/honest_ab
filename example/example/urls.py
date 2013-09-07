from django.conf.urls import patterns, include, url
from django.contrib import admin
from tested_app.views import BasicView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', BasicView.as_view(), name='home'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
