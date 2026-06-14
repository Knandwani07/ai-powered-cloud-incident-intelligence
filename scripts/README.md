# Scripts

This directory contains utility scripts used for testing and populating the incident intelligence platform with sample data.

## Directory Structure

```text
scripts/
│
└── seed-incidents.py
```

---

# Seed Incidents

The `seed-incidents.py` script generates realistic ECS incident records and uploads them to Amazon S3. These records simulate production incidents and provide sample data for analytics, AI processing, and reporting.

## Purpose

- Populate the S3 incident repository with sample data.
- Simulate common ECS task failures.
- Test the Athena analytics pipeline.
- Validate AI-powered reporting.
- Generate historical incident trends.
- Enable end-to-end testing without causing actual failures.

---

## Prerequisites

Before running the script:

- Configure AWS CLI credentials.
- Install Python 3.9 or later.
- Install the boto3 library.
- Replace both occurrences of `[your-account-id]` with your AWS account ID.
- Ensure the S3 bucket already exists.

## Install Dependencies

```bash
pip install boto3
```

---

## Run the Script

```bash
python seed-incidents.py
```

The script uploads 30 randomly generated incidents to Amazon S3.

Example output:

```text
Uploaded: incident-logs/2026-06-14/4f8d8a9b1c2d3e4f.json
Uploaded: incident-logs/2026-06-13/7a2e1c5d8b9f6a3c.json
...
Done! 30 incidents seeded.
```

---

## Generated Incident Types

The script randomly generates incidents from predefined scenarios.

| Stop Code | Incident Type | Description |
|------------|---------------|-------------|
| EssentialContainerExited | CONTAINER_CRASH | Container exited unexpectedly |
| OutOfMemoryError | OOM_KILL | Container exceeded memory limits |
| TaskFailedToStart | STARTUP_FAILURE | Task failed during startup |
| UserInitiated | MANUAL_STOP | Task intentionally stopped |

---

## Data Generated

Each incident record contains:

- Timestamp
- Task ARN
- Cluster ARN
- Stop code
- Stopped reason
- Incident type
- Raw event payload

Example:

```json
{
  "timestamp": "2026-06-14T10:15:23.456789",
  "task_arn": "arn:aws:ecs:ap-south-1:123456789012:task/incident-intel-cluster/4f8d8a9b1c2d3e4f",
  "cluster": "arn:aws:ecs:ap-south-1:123456789012:cluster/incident-intel-cluster",
  "stop_code": "OutOfMemoryError",
  "stopped_reason": "Container killed due to memory usage exceeding limit",
  "incident_type": "OOM_KILL",
  "raw_event": "{}"
}
```

---

## Storage Structure

Generated files are stored in Amazon S3 using date-based partitions.

```text
incident-logs/
│
├── 2026-06-14/
│   ├── 4f8d8a9b1c2d3e4f.json
│   ├── 9c7e6d5a4b3f2e1d.json
│
├── 2026-06-13/
│   ├── 8a1b2c3d4e5f6a7b.json
│
└── ...
```

---

## AWS Services Used

- Amazon S3
- Amazon ECS
- AWS SDK for Python (Boto3)

---

## Workflow

```text
Seed Script
      ↓
Generate Random Incident Data
      ↓
Create JSON Records
      ↓
Amazon S3
      ↓
Amazon Athena
      ↓
AI Incident Reporter
      ↓
Amazon Comprehend
      ↓
Amazon SNS
      ↓
Email Intelligence Report
```

---

## Features

- Generates realistic ECS incident scenarios.
- Creates random timestamps from the last seven days.
- Produces unique task identifiers.
- Uploads JSON records directly to Amazon S3.
- Enables Athena query testing.
- Supports AI-based trend analysis and reporting.
- Simplifies end-to-end validation of the incident intelligence platform.

---

## Use Cases

- Functional testing
- Athena query validation
- Dashboard visualization
- AI report generation
- Trend analysis
- Demonstration and learning purposes

> **Note:** This script generates synthetic incident data and is intended for testing and demonstration purposes only.
