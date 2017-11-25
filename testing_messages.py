import json
import unittest

from event import event


class TestInternalMessages(unittest.TestCase):

    def test_prepare(self):

        prepare_0 = Prepare(1,5)

        json = prepare_0.toJSON()

        recieved_message = MessageReader.fromJSON(json)

        self.assertEqual(received_message.n, 1)
        self.assertEqual(received_message.index, 5)



if __name__ == '__main__':
    unittest.main()
