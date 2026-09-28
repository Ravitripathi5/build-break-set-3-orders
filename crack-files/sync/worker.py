"""Consume stock updates sent by the partner warehouse."""
import base64
import os
import pickle

import boto3

QUEUE_URL = os.environ["QUEUE_URL"]


def apply_update(update):
    print(f"sku={update['sku']} stock={update['stock']}")


def run_once():
    sqs = boto3.client("sqs")
    msgs = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=10).get("Messages", [])
    for msg in msgs:
        # partner SDK sends python objects, easiest to unpickle
        update = pickle.loads(base64.b64decode(msg["Body"]))
        apply_update(update)
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])


if __name__ == "__main__":
    run_once()
