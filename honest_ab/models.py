from django.db import models
from django.template.defaultfilters import slugify

from honest_ab.binning_functions.base import binning_choices


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
    can only be associated with one experiment in an experiment layer.
    """

    active = models.BooleanField(default=True, help_text='Set to false if the instance is deleted.')

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True)

    def __unicode__(self):
        return self.slug


class Experiment(SlugReplacementMixin, models.Model):
    """
    An experiment is a single test. It requires a decision class, which is used
    to partition models into the experiment.
    """

    active = models.BooleanField(default=True, help_text='Set to false if the instance is deleted.')

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True)

    # This is 2 for a standard A/B test.
    number_of_classes = models.PositiveIntegerField(default=2)

    percentage_of_traffic = models.FloatField(
        verbose_name=u"Percentage of eligible traffic to be assigned to this experiment.  "
        u"Takes floating point value between 0 and 100",
        default=100.0
    )

    # Class to use as decision function. Should be subclass of
    # CachedExperimentBinningHandler
    decision_class = models.CharField(choices=binning_choices.choices, max_length=255)

    domain = models.ForeignKey(ExperimentDomain)

    def __unicode__(self):
        return self.slug


class ExperimentAllocation(models.Model):
    """
    Record of caching an experiment into 1 group for a single experiment.
    """

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    experiment = models.ForeignKey(Experiment)
    model = models.CharField(max_length=128)
    model_pk = models.BigIntegerField()
    classification = models.CharField(max_length=16)

    class Meta(object):
        unique_together = ('model_pk', 'model', 'experiment')

    def __unicode__(self):
        return "{0} {1} {2} {3}".format(self.experiment, self.model, self.model_pk, self.classification)


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
    date_modified = models.DateTimeField(auto_now=True)

    experiment_allocation = models.ForeignKey(ExperimentAllocation)
    goal = models.ForeignKey(Goal)
