# Lambda Functions

This directory contains the AWS Lambda functions used in the AI-Powered Cloud Incident Intelligence Platform.

These functions enable event-driven incident collection, AI-powered analysis, and automated reporting.

## Directory Structure

```text
lambda/
│
├── incident-log-exporter/
│   ├── lambda_function.py
│   └── README.md
│
├── incident-ai-reporter/
│   ├── lambda_function.py
│   └── README.md
│
└── README.md
```

## Components

### Incident Log Exporter

Captures ECS task stop events and stores incident information in Amazon S3 for further analysis.

**AWS Services Used**

- AWS Lambda
- Amazon EventBridge
- Amazon ECS
- Amazon S3

---

### AI Incident Reporter

Queries incident data using Amazon Athena, performs sentiment analysis using Amazon Comprehend, and sends intelligence reports through Amazon SNS.

**AWS Services Used**

- AWS Lambda
- Amazon Athena
- Amazon Comprehend
- Amazon SNS
- Amazon S3

---

## Workflow

```text
ECS Task Stop Event
        ↓
Amazon EventBridge
        ↓
Incident Log Exporter
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
Email Report
```

## Features

- Event-driven architecture
- Incident classification
- Centralized log storage
- AI-powered analysis
- Root cause identification
- Automated email reporting
- Serverless implementation
