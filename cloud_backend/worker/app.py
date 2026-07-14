import json
import os
from decimal import Decimal
from typing import Any

import boto3


dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)


def convert_numbers(value: Any) -> Any:
    """
    Convert Python float values into Decimal values because
    DynamoDB's Python SDK does not accept float objects directly.
    """

    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, dict):
        return {
            key: convert_numbers(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            convert_numbers(item)
            for item in value
        ]

    return value


def lambda_handler(event, context):
    failures = []

    for record in event.get("Records", []):
        message_id = record.get("messageId")

        try:
            payload = json.loads(record["body"])

            item = convert_numbers(payload)

            item["record_type"] = "telemetry"

            table.put_item(
                Item=item,
            )

            print(
                f"Stored telemetry for "
                f"{payload.get('machine_id')}"
            )

        except Exception as error:
            print(
                f"Worker failed for message "
                f"{message_id}: {error}"
            )

            failures.append({
                "itemIdentifier": message_id,
            })

    return {
        "batchItemFailures": failures,
    }