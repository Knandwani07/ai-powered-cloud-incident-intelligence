import boto3
import json
import datetime
import random
import uuid

s3 = boto3.client('s3', region_name='ap-south-1')
BUCKET = 'incident-intelligence-logs-[your-account-id]-ap-south-1'

incident_scenarios = [
    {
        "stop_code": "EssentialContainerExited",
        "stopped_reason": "Essential container in task exited",
        "incident_type": "CONTAINER_CRASH"
    },
    {
        "stop_code": "OutOfMemoryError",
        "stopped_reason": "Container killed due to memory usage exceeding limit",
        "incident_type": "OOM_KILL"
    },
    {
        "stop_code": "TaskFailedToStart",
        "stopped_reason": "ResourceInitializationError: unable to pull image",
        "incident_type": "STARTUP_FAILURE"
    },
    {
        "stop_code": "EssentialContainerExited",
        "stopped_reason": "Application crashed with exit code 137",
        "incident_type": "CONTAINER_CRASH"
    },
    {
        "stop_code": "UserInitiated",
        "stopped_reason": "Task stopped by user during deployment",
        "incident_type": "MANUAL_STOP"
    }
]

for i in range(30):
    days_ago = random.randint(0, 7)
    hours_ago = random.randint(0, 23)
    timestamp = (
        datetime.datetime.utcnow()
        - datetime.timedelta(days=days_ago, hours=hours_ago)
    ).isoformat()

    scenario = random.choice(incident_scenarios)
    task_id = str(uuid.uuid4()).replace('-', '')[:16]
    date_prefix = timestamp[:10]

    incident = {
        "timestamp": timestamp,
        "task_arn": f"arn:aws:ecs:ap-south-1:[your-account-id]:task/incident-intel-cluster/{task_id}",
        "cluster": "arn:aws:ecs:ap-south-1:[your-account-id]:cluster/incident-intel-cluster",
        "stop_code": scenario["stop_code"],
        "stopped_reason": scenario["stopped_reason"],
        "incident_type": scenario["incident_type"],
        "raw_event": "{}"
    }

    key = f"incident-logs/{date_prefix}/{task_id}.json"
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(incident),
        ContentType='application/json'
    )
    print(f"Uploaded: {key}")

print("Done! 30 incidents seeded.")
