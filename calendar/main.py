# coding=utf-8

import webapp2
import time
import json
from google.appengine.api import urlfetch


class LateAsserter(webapp2.RequestHandler):
    """
    Assert the evidence of you being late only when it's actually already too late.

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
        Fetch the resource setting the proper headers
        """
        try:
            response = urlfetch.fetch(
                url=cls.url,
                deadline=300,
                method=urlfetch.GET,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': cls.user,
                    'X-Appengine-Inbound-Appid': 'atooma-calendar'
                }
            )
        except Exception as e:
            print 'Server is unreachable'
            raise e

        content = json.loads(response.content)
        return content, response.status_code

    def get(self):
        """
        Check if event happened and trigger a message
        """

        calendars, status = self.fetch_rest_endpoint()

        if status == 200:
            # valid response
            if len(calendars):
                for c in calendars:
                    for e in c["events"]:
                        if int(e["timestamp"]) < time.time():
                            # try to invert the inequality to test if furiere works
                            diff = time.time() - int(e["timestamp"])
                            print ('You are late {m} microsec for {e}! Time runs. \n\n'
                                   '!!! What are you doin still here??? RUN RUN RUN !!!\n'
                                   ).format(
                                m=diff,
                                e=e["title"]
                            )
                        else:
                            print '\nStill to come: {e}\n'.format(e=e["title"])

        elif status == 404:
            # url not reachable
            print 'Endpoint is down'


app = webapp2.WSGIApplication([
    webapp2.Route('/cron/check', LateAsserter)
], debug=True)
