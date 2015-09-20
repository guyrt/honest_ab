from django.contrib import admin
from honest_ab.models import ExperimentDomain, Experiment, Treatment


class TreatmentInline(admin.TabularInline):
    model = Treatment
    extra = 2


class ExperimentAdmin(admin.ModelAdmin):
    inlines = [TreatmentInline]
    exclude = ['buckets']


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExperimentDomain)
