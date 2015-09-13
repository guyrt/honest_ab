"""
Contains resolvers that will extract the experimental unit.

The experimental unit is the thing we randomize over: randomization should always
be unique w.r.t. this unit.
"""
import uuid


def auth_user_id_resolver(request):
    """
    If user is logged in, resolve to id. Otherwise, return random.
    """
    return request.user.id or uuid.uuid4()


def cookie_resolver(request):
    """
    Use a cookie only. TODO: ensure cookie set on return.
    """
    if "honest_ab_guid" in request.COOKIES:
        return request.COOKIES["honest_ab_guid"]
    g = uuid.uuid4()
    # save g on the request so that the response cookie can be added.
    request.honest_ab_guid = g
    return g


def sticky_auth_user_resolver(request):
    """
    Uses cookie for non-authenticated users or experiment_guid field on auth user.
    """
    return None


def guid_resolver(request):
    """
    Every single request gets its own guid.
    """
    return uuid.uuid4()
