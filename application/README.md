# Application

This directory contains the web application files and Docker configuration used to deploy the frontend of the AI-Powered Cloud Incident Intelligence Platform.

The application is packaged as a lightweight container and deployed on Amazon ECS Fargate. It provides a simple landing page that represents the platform and highlights the core AWS services used in the solution.

## Directory Structure

```text
application/
│
├── index.html
└── Dockerfile
```

## Files

### index.html

The `index.html` file contains the static web page displayed by the application. It provides:

- Project title and description
- Information about the self-healing infrastructure
- Visual badges representing key AWS services:
  - Amazon ECS Fargate
  - Amazon Comprehend
  - Amazon Athena
  - Amazon S3

### Dockerfile

The Dockerfile defines the container image used to run the application.

It performs the following actions:

1. Uses the lightweight `nginx:alpine` image as the base image.
2. Copies the `index.html` file into the default Nginx web directory.
3. Exposes port `80` for HTTP traffic.
4. Starts the Nginx web server.

## Container Configuration

Base Image:

```dockerfile
nginx:alpine
```

Exposed Port:

```text
80
```

Web Server:

```text
Nginx
```

## Build the Docker Image

From the `application` directory, run:

```bash
docker build -t incident-intel-app .
```

## Run the Container Locally

```bash
docker run -d -p 80:80 incident-intel-app
```

## Verify the Application

Open the following URL in a browser:

```text
http://localhost
```

The page displays the **AI-Powered Cloud Incident Intelligence Platform** landing page along with the AWS services utilized in the solution.

## Deployment

The container image is pushed to Amazon Elastic Container Registry (ECR) and deployed on Amazon ECS Fargate as part of the complete cloud incident intelligence platform.

## Technologies Used

- HTML
- CSS
- Docker
- Nginx
- Amazon ECR
- Amazon ECS Fargate
