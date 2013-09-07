from django.contrib import admin
from honest_ab.forms import ExperimentForm
from honest_ab.models import Experiment, ExperimentAllocation, ExperimentDomain, GoalAchieved, Goal


class ExperimentDomainAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    fields = ('name', 'active', 'slug')
    list_display = fields
    search_fields = ('slug', )
    list_filter = ('active', )


class ExperimentAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    fields = ('name', 'active', 'slug', 'domain', 'decision_class', 'number_of_classes', 'percentage_of_traffic')
    list_display = fields
    search_fields = ('slug', 'decision_class')
    list_filter = ('active', 'decision_class', 'domain')
    form = ExperimentForm


class ExperimentAllocationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    fields = ('experiment', 'model', 'model_pk', 'classification')
    list_display = fields
    list_select_related = True
    search_fields = ('experiment__slug', 'model', 'model_pk')
    list_filter = ('experiment__slug', 'model')


class GoalAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    fields = ('name', 'slug', 'active')
    list_display = fields
    search_fields = ('slug', 'name')
    list_filter = ('active', )


class GoalAchievedAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    fields = ('goal', 'experiment_allocation')
    list_display = fields
    list_filter = ('goal', )
    search_fields = ('goal', )


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExperimentDomain, ExperimentDomainAdmin)
admin.site.register(ExperimentAllocation, ExperimentAllocationAdmin)
admin.site.register(GoalAchieved)
admin.site.register(Goal, GoalAdmin)
