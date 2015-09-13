from django.db import models
from django.template.defaultfilters import slugify


class SlugReplacementMixin(object):

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.slug:
            self.slug = slugify(self.name)
            i = 0
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.name) + '_' + str(i)
        super(SlugReplacementMixin, self).save(force_insert, force_update, using)


class ExperimentDomain(SlugReplacementMixin, models.Model):
    """
    An experiment domain is a set of experiments that are non-overlapping. A model
    can only be associated with one experiment in an experiment domain.
    """

    active = models.BooleanField(default=True, help_text='Set to false if the instance is deleted.')

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128, help_text="Human readable name.")
    slug = models.SlugField(max_length=64, unique=True, help_text="Used as salt. Must be unique.")
    num_buckets = models.PositiveIntegerField(default=1000)

    experimental_unit_resolver = models.CharField(max_length=255)

    def __unicode__(self):
        return "domain {0} using {1}".format(self.name, self.decision_class)


class Experiment(SlugReplacementMixin, models.Model):
    """
    An experiment is a single test. It requires a decision class, which is used
    to partition models into the experiment.
    """

    active = models.BooleanField(default=True, help_text='Set to false if the instance is deleted.')

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True, name="Experiment-specific salt")

    percentage_of_traffic = models.FloatField(
        verbose_name=u"Percentage of eligible traffic to be assigned to this experiment.  "
        u"Takes floating point value between 0 and 100",
        default=100.0
    )

    domain = models.ForeignKey(ExperimentDomain)
    buckets = models.CharField(max_length=255)  # todo - set these on save?

    def __unicode__(self):
        return self.slug


class Treatment(models.Model):

    active = models.BooleanField(default=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    percentage_of_traffic = models.FloatField(
        verbose_name="By default, this is set to 1/N for N treatments in an experiment",
        default=None
    )

    name = models.CharField(max_length=255)

"""
Handle goals, which is an optional feature for tracking specific actions.
"""


class Goal(SlugReplacementMixin, models.Model):
    """
    Explicit goal for an experiment. An example might be clicking an element on the page or
    creating a blog post.

    Goals should be set from the admin.
    """

    active = models.BooleanField(default=True, help_text='Set to false if the instance is deleted.')

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True)


class GoalAchieved(models.Model):
    """
    A GoalAchieved entry records when a goal occurs for a specific experiment allocation.

    See methods in api.py for helpers to write a GoalAchived entry.
    """

    date_added = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey(Goal)
