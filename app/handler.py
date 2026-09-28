"""Order Intake - consumes orders from SQS and records accepted orders in DynamoDB."""
import json
import os
import time

TABLE_NAME = os.environ.get("TABLE_NAME", "")
APP_VERSION = os.environ.get("APP_VERSION", "dev")

_table = None


def table():
    global _table
    if _table is None:
        import boto3

        _table = boto3.resource("dynamodb").Table(TABLE_NAME)
    return _table


def validate(order):
    if not isinstance(order.get("order_id"), str) or not order["order_id"]:
        raise ValueError("order_id is required")
    if not isinstance(order.get("sku"), str) or not order["sku"]:
        raise ValueError("sku is required")
    qty = order.get("qty")
    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("qty must be a positive integer")


def lambda_handler(event, context):
    accepted = []
    for record in event.get("Records", []):
        order = json.loads(record["body"])
        validate(order)
        table().put_item(
            Item={
                "order_id": order["order_id"],
                "sku": order["sku"],
                "qty": order["qty"],
                "status": "ACCEPTED",
                "accepted_at": int(time.time()),
                "version": APP_VERSION,
            }
        )
        accepted.append(order["order_id"])
    return {"accepted": accepted}
