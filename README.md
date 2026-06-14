# AWS Incident Intelligence Platform

An AI-powered cloud incident intelligence platform built on AWS that provides automated incident detection, self-healing capabilities, AI-driven log analysis, and daily incident reporting.

The solution leverages Amazon ECS Fargate, AWS Lambda, Amazon EventBridge, Amazon Athena, Amazon Comprehend, Amazon SNS, and Amazon CloudWatch to create a resilient and intelligent monitoring system for containerized applications.

---

## Architecture

<img width="1920" height="1088" alt="export (15)" src="https://github.com/user-attachments/assets/133cc8f3-e1bd-44f9-880d-2d9cb1814909" />


---

## Features

- Self-healing containerized infrastructure
- Automatic ECS task recovery
- Real-time incident detection
- Event-driven automation using EventBridge
- Centralized incident storage in Amazon S3
- SQL-based analytics with Amazon Athena
- AI-powered incident analysis using Amazon Comprehend
- Email notifications using Amazon SNS
- CloudWatch alarms and monitoring dashboards
- Daily automated incident intelligence reports

---

## AWS Services Used

| Service | Purpose |
|----------|----------|
| Amazon ECS Fargate | Container orchestration |
| Amazon ECR | Container image repository |
| Amazon VPC | Network isolation |
| Application Load Balancer | Traffic distribution |
| Amazon EventBridge | Event-driven automation |
| AWS Lambda | Incident processing |
| Amazon S3 | Incident data lake |
| Amazon Athena | Incident analytics |
| Amazon Comprehend | AI-powered analysis |
| Amazon SNS | Email notifications |
| Amazon CloudWatch | Monitoring and observability |
| IAM | Access control and security |

---

## Architecture Components

### Self-Healing Infrastructure

- Amazon VPC
- Public and Private Subnets
- Internet Gateway
- NAT Gateway
- Application Load Balancer
- Amazon ECS Fargate
- ECS Tasks
- Amazon ECR
- Auto Scaling Policies
- Amazon CloudWatch

### AI Incident Intelligence Pipeline

- ECS Task Stop Events
- Amazon EventBridge
- AWS Lambda
- Amazon S3
- Amazon Athena
- Amazon Comprehend
- Amazon SNS


---

## Project Structure

```text
ai-powered-cloud-incident-intelligence/
│
├── application/
│   ├── Dockerfile
│   ├── index.html
│   └── README.md
│
├── athena/
│   └── athena-queries.md
│
├── lambda/
│   ├── incident-ai-reporter/
│   │   ├── lambda_function.py
│   │   └── README.md
│   │
│   ├── incident-log-exporter/
│   │   ├── lambda_function.py
│   │   └── README.md
│   │
│   └── README.md
│
├── scripts/
│   ├── seed-incidents.py
│   └── README.md
│
└── README.md
```


---

## Project Outcomes

- Built a production-ready containerized application using Amazon ECS Fargate.
- Implemented self-healing capabilities for improved reliability.
- Created an incident data warehouse using Amazon S3 and Athena.
- Performed AI-driven incident analysis using Amazon Comprehend.
- Automated event processing with Lambda and EventBridge.
- Configured real-time notifications using Amazon SNS.
- Developed monitoring dashboards using CloudWatch.
- Validated end-to-end system functionality through testing.

---

## Conclusion

This project demonstrates the implementation of an AI-powered cloud incident intelligence platform using AWS managed services. The solution enables automated incident detection, intelligent analysis, self-healing mechanisms, and proactive reporting, thereby improving system reliability and operational efficiency.
