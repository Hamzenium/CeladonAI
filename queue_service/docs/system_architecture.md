# System Architecture for Metadata Processing Application

## Overview
This document provides an in-depth explanation of the system architecture for the Metadata Processing Application. The application is designed to consume metadata from a RabbitMQ queue, download files from an S3 bucket or a given URL, process the files, and extract text content into manageable chunks.

---

## Architecture Diagram

The following diagram outlines the architecture of the system:

```
+------------------+                     +------------------+
|  RabbitMQ Queue  |-------------------->|   Application    |
| (metadata_queue) |                     |  (Go Service)    |
+------------------+                     +------------------+
           |                                      |
           |                                      v
           |                          +-------------------+
           |                          |  Temporary Files  |
           |                          |   (Local Disk)    |
           |                          +-------------------+
           |                                      |
           |                                      v
           |                          +-------------------+
           |                          |       S3          |
           |------------------------->| (Custom Endpoint) |
           |                          +-------------------+
           |                                      |
           |                                      v
           |                          +-------------------+
           |                          |     Processed     |
           |                          |     Results       |
           +------------------------->|    (Database)     |
                                      +-------------------+
```
---

## Detailed Components

### 1. **RabbitMQ**
- **Purpose**: Acts as a message broker for metadata delivery.
- **Details**:
  - Metadata messages are JSON objects containing:
    - `email`: The user's email.
    - `file_url`: A direct URL to the file.
    - `s3_key`: The S3 object key used for retrieval.
  - Configurations:
    - RabbitMQ connection URL: `amqps://admin:<password>@<host>:<port>`
    - Queue Name: `metadata_queue`

### 2. **Application (Go Service)**
- **Purpose**: The main processing engine that consumes messages, downloads files, processes content, and stores results.
- **Details**:
  - **Modules**:
    - `startConsumer`: Connects to RabbitMQ and consumes messages from the `metadata_queue`.
    - `processFile`: Downloads files from URLs or S3 buckets.
    - `processDownloadedFile`: Extracts text content from PDFs.
    - `splitTextIntoChunks`: Divides extracted text into manageable chunks.
  - **Key Libraries**:
    - `pdf`: For reading and extracting text from PDF files.
    - `aws-sdk-go-v2`: For connecting to S3.
    - `rabbitmq/amqp091-go`: For RabbitMQ integration.

### 3. **Temporary Files (Local Disk)**
- **Purpose**: Intermediate storage for downloaded files before processing.
- **Details**:
  - Files are downloaded to `./temp`.
  - Temporary files are deleted after processing.

### 4. **S3 Storage**
- **Purpose**: Stores files for long-term access.
- **Details**:
  - Bucket Name: `user-files-storage`
  - Endpoint: `https://3plvis.stackhero-network.com`
  - Configurations:
    - Region: `us-east-1`
    - Path-Style Addressing: Enabled.

### 5. **Processing Results**
- **Purpose**: Stores processed text chunks for further analysis or user retrieval.
- **Details**:
  - Results can be stored in a database for later use.
  - Each chunk contains approximately 200 words.

---

## Data Flow

1. **Metadata Reception**:
   - RabbitMQ sends metadata messages to the application.

2. **File Retrieval**:
   - The application downloads files from the provided URL or S3 bucket.

3. **Processing**:
   - Files are processed to extract text using the `pdf` library.
   - Text is split into chunks of 200 words each.

4. **Cleanup**:
   - Temporary files are removed from local storage.

5. **Result Storage**:
   - Processed chunks are stored in a database for future access.

---

## Key Notes

1. **Scalability**:
   - The application can be horizontally scaled by adding more instances of the Go service to process messages in parallel.

2. **Fault Tolerance**:
   - RabbitMQ ensures reliable delivery of messages.
   - Errors during file processing are logged for troubleshooting.

3. **Security**:
   - S3 access is secured using AWS credentials.
   - RabbitMQ communication uses SSL for encryption.

---

## Future Enhancements

- **Database Integration**:
  - Store processed chunks in a relational or NoSQL database.
- **Enhanced Monitoring**:
  - Add logging and monitoring tools such as Prometheus and Grafana.
- **Multi-Format Support**:
  - Extend support to file formats other than PDFs.
- **Distributed Processing**:
  - Utilize distributed task queues for large-scale processing.

