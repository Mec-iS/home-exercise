# coding=utf-8

import webapp2
import json
import twitter

from tw_secret import *

#
# Create a Twitter API object for authentication.
# Subscribe an app at <https://dev.twitter.com> to get keys.
#
api = twitter.Api(consumer_key=con_secret,
                  consumer_secret=con_secret_key,
                  access_token_key=token,
                  access_token_secret=token_key,
                  cache=None)


class MainHandler(webapp2.RequestHandler):
    def get(self, count=None):
        """
        Print on the screen part of the Atooma timeline: 10 or ``count``

        :param count: if the requested count is specified in the path, default to None
        """
        if count is not None:
            try:
                count = int(count)
            except ValueError:
                response = json.dumps({'error': 'count must be a int'})
                return self.response.write(response)

            tl = api.GetUserTimeline(screen_name='Atooma_Team', count=count)
            return self.response.write(tl)
        tl = api.GetUserTimeline(screen_name='Atooma_Team', count=10)
        return self.response.write(tl)

app = webapp2.WSGIApplication([
    webapp2.Route('/twitter/news/<count:[0-9]+>', MainHandler),
    webapp2.Route('/twitter/news', MainHandler),
], debug=True)
