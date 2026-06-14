# AI Incident Reporter

The AI Incident Reporter Lambda function generates intelligence reports by analyzing historical incident data stored in Amazon S3 and queried through Amazon Athena.

It leverages Amazon Comprehend for sentiment analysis and Amazon SNS for email notifications.

## Purpose

- Analyze incident trends.
- Perform sentiment analysis.
- Generate root cause analysis.
- Provide prioritized recommendations.
- Deliver automated email reports.

## Trigger

Amazon EventBridge Scheduler

**Schedule**

```text
Every 24 Hours
```

The function can also be invoked manually for testing purposes.

## Environment Variables

| Variable | Description |
|------------|------------|
| BUCKET_NAME | S3 bucket used for Athena query results |
| SNS_ARN | ARN of the SNS topic used for notifications |

## Analysis Components

### Amazon Athena

Queries incident data to retrieve:

- Total incidents
- Incident frequency
- Recent incidents
- Historical trends

### Amazon Comprehend

Performs sentiment analysis and generates health signals:

- POSITIVE
- NEGATIVE
- NEUTRAL
- MIXED

### Root Cause Analysis

The function identifies probable causes for:

- CONTAINER_CRASH
- STARTUP_FAILURE
- OOM_KILL
- MANUAL_STOP
- UNKNOWN

### Recommendations

Based on detected incidents, the report provides:

- High-priority actions
- Medium-priority actions
- Low-priority actions

## Report Contents

- Executive Summary
- Risk Assessment
- Incident Metrics
- Trend Analysis
- NLP Sentiment Scores
- Root Cause Analysis
- Prioritized Recommendations
- Infrastructure Status

## Notification Channel

Amazon SNS Email Subscription

Example Subject:

```text
[INCIDENT REPORT] AWS ECS Fargate | YYYY-MM-DD | ap-south-1
```

## AWS Services Used

- AWS Lambda
- Amazon Athena
- Amazon Comprehend
- Amazon SNS
- Amazon S3

## Workflow

```text
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
Email Report
```

## Features

- Automated report generation
- Trend analysis
- AI-powered sentiment analysis
- Root cause identification
- Risk assessment
- Prioritized recommendations
- Daily email notifications
- Serverless architecture
