# coding=utf-8

import webapp2
import time
import json
from google.appengine.api import urlfetch


class LateAsserter(webapp2.RequestHandler):
    """
    Assert the obviousness of being late only when it's actually already too late.

    Response expected format:
        ``[
            { "id": "birthdays", "owner": "server@application.net",
            [ { "title": "Fabrizio Birthday", "timestamp": 1464739200 }, ... ] }
        ]``
    """

    user = 'a.petreri@atooma.com'
    url = 'https://atooma-homework.appspot.com/calendars'

    @classmethod
    def fetch_rest_endpoint(cls):
        """
        Fetch the resource setting the proper headers.
        """
        try:
            response = urlfetch.fetch(
                url=cls.url,
                deadline=300,
                method=urlfetch.GET,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': cls.user,
                    'X-Appengine-Inbound-Appid': 'calendar-furiere'
                }
            )
        except Exception as e:
            print 'Server is unreachable'
            raise e

        content = json.loads(response.content)
        return content, response.status_code

    def get(self):
        """
        Check if event happened and trigger a message.
        """
        calendars, status = self.fetch_rest_endpoint()

        if status == 200:
            # valid response
            if len(calendars):
                # create a generator to avoid multiple for-looping
                events = (
                    (e["title"], abs(time.time() - int(e["timestamp"])), int(e["timestamp"]) < time.time())
                    for c in calendars
                    for e in c["events"]
                )
                # consume the generator to find if the event is passed or not
                while True:
                    try:
                        title, diff, is_passed = next(events)
                        if is_passed:
                            # event is in the past
                            print 'You are late {m} secs for {e}! Time runs. \n\n'.format(
                                m=diff,
                                e=title
                            )
                        else:
                            # event is in the future
                            print '\nKeep cool! Still to come: {e} in {m} secs\n'.format(
                                e=title,
                                m=diff
                            )

                    except StopIteration:
                        break
        elif status == 404:
            # url not reachable
            print 'Endpoint is down'


app = webapp2.WSGIApplication([
    webapp2.Route('/cron/check', LateAsserter)
], debug=True)
