import json
import boto3
import datetime
import os

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    task_arn = event.get('detail', {}).get('taskArn', 'unknown')
    stop_code = event.get('detail', {}).get('stopCode', 'unknown')
    stopped_reason = event.get('detail', {}).get('stoppedReason', 'unknown')
    cluster = event.get('detail', {}).get('clusterArn', 'unknown')
    timestamp = datetime.datetime.utcnow().isoformat()

    incident = {
        "timestamp": timestamp,
        "task_arn": task_arn,
        "cluster": cluster,
        "stop_code": stop_code,
        "stopped_reason": stopped_reason,
        "incident_type": classify_incident(stop_code),
        "raw_event": json.dumps(event)
    }

    date_prefix = timestamp[:10]
    key = f"incident-logs/{date_prefix}/{task_arn.split('/')[-1]}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(incident),
        ContentType='application/json'
    )
    return {"statusCode": 200, "body": "Incident logged"}

def classify_incident(stop_code):
    codes = {
        "TaskFailedToStart": "STARTUP_FAILURE",
        "EssentialContainerExited": "CONTAINER_CRASH",
        "OutOfMemoryError": "OOM_KILL",
        "UserInitiated": "MANUAL_STOP"
    }
    return codes.get(stop_code, "UNKNOWN")
