# coding=utf-8
import time
__author__ = 'Lorenzo'


def generate_events():
    events = []
    for i in xrange(7):
        events.append({"event-" + str(i): time.time() + 1000 * i})
    return events

print generate_events()

