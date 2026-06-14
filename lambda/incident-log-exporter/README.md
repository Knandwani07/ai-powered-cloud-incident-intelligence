# Incident Log Exporter

The Incident Log Exporter Lambda function captures Amazon ECS task stop events and stores incident details in Amazon S3.

## Purpose

- Detect task failures.
- Extract ECS task information.
- Classify incidents based on stop codes.
- Store incident records in JSON format.
- Build an incident data repository for analytics.

## Trigger

Amazon EventBridge Rule

**Event Source**

- Amazon ECS

**Event Type**

- Task State Change

## Environment Variables

| Variable | Description |
|------------|------------|
| BUCKET_NAME | S3 bucket used to store incident logs |

## Incident Classification

| Stop Code | Incident Type |
|------------|---------------|
| TaskFailedToStart | STARTUP_FAILURE |
| EssentialContainerExited | CONTAINER_CRASH |
| OutOfMemoryError | OOM_KILL |
| UserInitiated | MANUAL_STOP |
| Others | UNKNOWN |

## Output Location

```text
incident-logs/YYYY-MM-DD/<task-id>.json
```

Example:

```text
incident-logs/2026-06-14/123456789.json
```

## AWS Services Used

- AWS Lambda
- Amazon EventBridge
- Amazon ECS
- Amazon S3

## Workflow

```text
ECS Task Stop Event
        ↓
Amazon EventBridge
        ↓
Incident Log Exporter
        ↓
Amazon S3
```

## Features

- Automatic incident collection
- Incident classification
- JSON log generation
- S3-based data storage
- Event-driven processing
- Serverless architecture
