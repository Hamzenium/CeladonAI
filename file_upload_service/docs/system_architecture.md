# Architecture and System Overview

## Table of Contents
- [System Architecture](#system-architecture)
- [Key Components](#key-components)
- [Data Flow](#data-flow)
- [Interaction Between Components](#interaction-between-components)
- [Scalability and Fault Tolerance](#scalability-and-fault-tolerance)
- [Diagram](#diagram)

---

## System Architecture
The system is designed to be modular and distributed, integrating:
- **Flask** as the web application framework.
- **AWS S3** for file storage.
- **RabbitMQ** for asynchronous messaging.
- A CI/CD pipeline for automated testing and deployment.

The system architecture ensures:
1. Separation of concerns.
2. Extensibility for future integrations.
3. Scalability to handle increasing workloads.

---

## Key Components
### 1. **Flask Application**
- Acts as the entry point for all user interactions.
- Provides APIs for:
  - File uploads.
  - Metadata submission to RabbitMQ.
- Includes built-in error handling and response formatting.

### 2. **AWS S3 Integration**
- Stores uploaded files securely.
- Supports file versioning and accessibility using pre-signed URLs.

### 3. **RabbitMQ Integration**
- Handles asynchronous communication between services.
- Ensures decoupling of metadata processing from the main application logic.

### 4. **CI/CD Pipeline**
- Automates testing, linting, and deployment.
- Triggered manually via `workflow_dispatch` in GitHub Actions.

---

## Data Flow
### Step-by-Step Process:
1. **File Upload**
   - Users upload a file via the Flask API.
   - The file is temporarily stored on the local server and uploaded to AWS S3.

2. **Generate File URL**
   - The application generates a pre-signed URL for the uploaded file in S3.

3. **Metadata Submission**
   - Metadata (e.g., email, file URL) is sent to RabbitMQ for further processing.

4. **Asynchronous Processing**
   - A separate consumer (not part of this project) can process messages from RabbitMQ for downstream tasks.

---

## Interaction Between Components
### 1. **Flask and S3**
- Flask interacts with S3 using the `boto3` library.
- Each file is uploaded to a specific bucket, and a pre-signed URL is generated for user access.

### 2. **Flask and RabbitMQ**
- Flask publishes metadata messages to a RabbitMQ queue.
- The `aio-pika` library handles asynchronous message publishing, ensuring non-blocking operations.

### 3. **User Interaction**
- Users interact with Flask endpoints to upload files and retrieve status updates.

---

## Scalability and Fault Tolerance
### Scalability
- **Flask**: Can be scaled horizontally using WSGI servers like Gunicorn and load balancers.
- **AWS S3**: Highly scalable object storage capable of handling large files and high traffic.
- **RabbitMQ**: Supports clustering to handle increased messaging workloads.

### Fault Tolerance
- **AWS S3**: Ensures durability and availability of files with multi-region replication.
- **RabbitMQ**: Offers message persistence and delivery acknowledgments to avoid data loss.
- **Flask**: Includes error handling for predictable failures (e.g., invalid input).

---

## Diagram
Here is a simplified architecture diagram of the system:

```plaintext
+--------------+        +-----------------+       +----------------+
|   User/API   | ---->  |    Flask App    | --->  |  RabbitMQ Queue |
+--------------+        +-----------------+       +----------------+
                            |                           |
                            |                           v
                            v                     +----------------+
                      +-----------------+         |  Consumer App  |
                      |      AWS S3     |         +----------------+
                      +-----------------+
```

---

