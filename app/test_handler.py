import json
import unittest

import handler


class FakeTable:
    def __init__(self):
        self.items = {}

    def put_item(self, Item):
        self.items[Item["order_id"]] = Item


def sqs_event(*bodies):
    return {"Records": [{"body": json.dumps(b)} for b in bodies]}


class OrdersTest(unittest.TestCase):
    def setUp(self):
        handler._table = FakeTable()

    def test_accepts_valid_order(self):
        out = handler.lambda_handler(sqs_event({"order_id": "o-1", "sku": "HAMMER", "qty": 2}), None)
        self.assertEqual(out["accepted"], ["o-1"])
        self.assertEqual(handler._table.items["o-1"]["status"], "ACCEPTED")

    def test_rejects_bad_qty(self):
        with self.assertRaises(ValueError):
            handler.lambda_handler(sqs_event({"order_id": "o-2", "sku": "SAW", "qty": 0}), None)

    def test_rejects_missing_sku(self):
        with self.assertRaises(ValueError):
            handler.lambda_handler(sqs_event({"order_id": "o-3", "qty": 1}), None)


if __name__ == "__main__":
    unittest.main()
