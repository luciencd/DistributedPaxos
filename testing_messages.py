import json
import unittest
from datetime import datetime, date
from dateutil import tz
from dateutil.parser import parse
from message import *
from event import event,EventTypes



class TestInternalMessages(unittest.TestCase):

    def test_prepare(self):

        prepare_0 = Prepare(0)
        json = prepare_0.toJSON()
        received_message = MessageReader.fromJSON(json)

        self.assertEqual(received_message.n, 0)

    def test_promise_first_round(self):
        #first proposal
        now_time = datetime.utcnow()
        now_time = now_time.replace(tzinfo=tz.tzutc()).replace(microsecond=0)
        e = event(0,EventTypes.TWEET,"Sad. Bad!",now_time,"Trump",0)

        promise_0 = Promise(None,None,0)
        json = promise_0.toJSON()
        received_message = MessageReader.fromJSON(json)

        self.assertEqual(received_message.n, None)

    def test_promise_second_round(self):
        #first proposal
        now_time = datetime.utcnow().replace(tzinfo=tz.tzutc()).replace(microsecond=0).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        ##bug where we would never send the tweet directly after setting its time to have a timezone.
        e0 = event(0,EventTypes.TWEET,"Sad. Bad!",now_time,"Trump",0)##apparently, now_time has to be int in order to be sent.

        promise_1 = Promise(0,e0,0)
        json = promise_1.toJSON()
        promise_received = MessageReader.fromJSON(json.strip())

        self.assertEqual(promise_received.n, 0)
        self.assertEqual(promise_received.i, 0)
        self.assertTrue(promise_received.v.site == e0.site and \
                        promise_received.v.op == e0.op and \
                        promise_received.v.data == e0.data and \
                        promise_received.v.truetime == e0.truetime and \
                        promise_received.v.name == e0.name and \
                        promise_received.v.timestamp == e0.timestamp)

    '''def test_accept_second_round(self):
        #first proposal
        now_time = datetime.utcnow().replace(tzinfo=tz.tzutc()).replace(microsecond=0).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')
        ##bug where we would never send the tweet directly after setting its time to have a timezone.
        e0 = event(0,EventTypes.TWEET,"Sad. Bad!",now_time,"Trump",0)##apparently, now_time has to be int in order to be sent.

        accept_request_1 = acceptRequest(0,e0,0)
        json = accept_request_1.toJSON()
        accept_request_received = MessageReader.fromJSON(json.strip())

        self.assertEqual(accept_request_received.n, 0)
        self.assertEqual(accept_request_received.i, 0)
        self.assertTrue(accept_request_received.v.site == e0.site and \
                        accept_request_received.v.op == e0.op and \
                        accept_request_received.v.data == e0.data and \
                        accept_request_received.v.truetime == e0.truetime and \
                        accept_request_received.v.name == e0.name and \
                        accept_request_received.v.timestamp == e0.timestamp)'''




if __name__ == '__main__':
    unittest.main()
