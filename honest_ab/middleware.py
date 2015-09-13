from honest_ab.resolver import get_resolver


class HonestABMiddleware(object):

    def process_request(self, request):
        """
        Attach a resolver to the request.
        """
        request.honest_ab_resolver = get_resolver(request)

    def process_response(self, request, response):
        """
        If resolver is cookie type then ensure cookies are stored.
        """
        return response
        # if not hasattr(response, 'context_data'):
        #     return response
        #
        # if HONEST_AB_COOKIE_KEY in response.context_data:
        #     for key, value in response.context_data[HONEST_AB_COOKIE_KEY]['__cache__'].iteritems():
        #         response.set_signed_cookie(key, value['value'], salt=value['salt'])
        #
        # return response
