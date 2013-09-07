from importlib import import_module
from honest_ab.binning_functions.base import HONEST_AB_SKIP_TYPE, HONEST_AB_COOKIE_KEY

from honest_ab.models import Experiment, GoalAchieved, Goal, ExperimentAllocation


class ImproperlyConfigured(Exception):
    pass


def _get_backend_class(import_path):
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't an honest_ab backend module." % import_path)
    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing honest_ab backend module %s: "%s"' % (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Honest_ab backend module "%s" does not define a "%s" class.' % (module, classname))


def _fake_return_context(experiment_slug, context):
    if not context:
        context = dict()
    if HONEST_AB_COOKIE_KEY not in context:
        context[HONEST_AB_COOKIE_KEY] = dict()

    context[HONEST_AB_COOKIE_KEY][experiment_slug] = HONEST_AB_SKIP_TYPE
    if '__cache__' not in context[HONEST_AB_COOKIE_KEY]:
        context[HONEST_AB_COOKIE_KEY]['__cache__'] = dict()
    return context


def get_experiment_bin(obj, experiment_slug, request=None, context=None):
    """
    Retrieve bin for an Experiment and an object.
    """
    try:
        experiment = Experiment.objects.get(slug=experiment_slug)
    except Experiment.DoesNotExist:
        return _fake_return_context(experiment_slug, context)

    if experiment.active:
        bin_obj = _get_backend_class(experiment.decision_class)()
        return bin_obj.bin(obj, experiment, request, context)
    else:
        return _fake_return_context(experiment_slug, context)


def goal_achieved(goal_id=None, goal_slug=None, **kwargs):
    """
    Record instance of a goal being achieved.

    goal_id or goal_slug is required. Note that passing goal_slug requires an extra database query.

    Optional parameters allow the method to identify which experiment allocation to use.
        experiment_allocation_id: used directly. No additional database calls.
    """

    if not goal_id:
        try:
            goal_id = Goal.objects.filter(slug=goal_slug).values_list('id', flat=True)[0]
        except IndexError:
            raise Goal.DoesNotExist()

    if 'experiment_allocation_id' in kwargs:
        GoalAchieved.objects.create(
            experiment_allocation_id=kwargs['experiment_allocation_id'],
            goal_id=goal_id
        )
    elif 'model' in kwargs and 'model_pk' in kwargs:
        experiment_allocation_ids = ExperimentAllocation.objects.filter(
            model=kwargs['model'],
            model_pk=kwargs['model_pk']
        ).exclude(group=HONEST_AB_SKIP_TYPE).values_list('id', flat=True)
        for experiment_allocation_id in experiment_allocation_ids:
            GoalAchieved.objects.create(
                experiment_allocation_id=experiment_allocation_id,
                goal_id=goal_id
            )
    else:
        raise ValueError("Unable to identify goal and experiment allocation.")
