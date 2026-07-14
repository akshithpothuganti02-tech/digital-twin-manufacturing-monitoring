import json
import os
from typing import Any

import boto3


sqs = boto3.client("sqs")

QUEUE_URL = os.environ["QUEUE_URL"]


def build_response(
    status_code: int,
    body: dict[str, Any],
) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    try:
        raw_body = event.get("body")

        if raw_body is None:
            return build_response(
                400,
                {
                    "message": "Request body is required",
                },
            )

        if isinstance(raw_body, str):
            payload = json.loads(raw_body)
        else:
            payload = raw_body

        required_fields = [
            "machine_id",
            "machine_name",
            "temperature",
            "vibration",
            "power",
            "rpm",
            "pressure",
            "timestamp",
            "health_score",
            "status",
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in payload
        ]

        if missing_fields:
            return build_response(
                400,
                {
                    "message": "Missing required fields",
                    "missing_fields": missing_fields,
                },
            )

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(payload),
        )

        return build_response(
            202,
            {
                "message": "Telemetry accepted for processing",
                "machine_id": payload["machine_id"],
            },
        )

    except json.JSONDecodeError:
        return build_response(
            400,
            {
                "message": "Request body is not valid JSON",
            },
        )

    except Exception as error:
        print(f"Ingestion error: {error}")

        return build_response(
            500,
            {
                "message": "Internal ingestion error",
            },
        )