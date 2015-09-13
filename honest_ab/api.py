from honest_ab.models import GoalAchieved, Goal


def goal_achieved(goal_id=None, goal_slug=None):
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


    GoalAchieved.objects.create(
        goal_id=goal_id
    )
