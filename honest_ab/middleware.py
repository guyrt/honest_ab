from binning_functions.base import HONEST_AB_COOKIE_KEY


class HonestABMiddleware(object):

    def process_response(self, request, response):
        """
        If response context has an "honest_experiments" element,
         create cookies.
        """
        if not hasattr(response, 'context_data'):
            return response

        if HONEST_AB_COOKIE_KEY in response.context_data:
            for key, value in response.context_data[HONEST_AB_COOKIE_KEY]['__cache__'].iteritems():
                response.set_signed_cookie(key, value['value'], salt=value['salt'])

        return response
