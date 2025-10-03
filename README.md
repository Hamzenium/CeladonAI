CeladonAI

https://github.com/user-attachments/assets/52025219-c9f6-438e-8944-cbe7636f10ac


# **Microservices System**

A distributed system consisting of multiple microservices, designed for scalability, modularity, and maintainability. This project follows a modern microservices architecture with each service addressing a specific functionality.

---

## **Table of Contents**
- [High-Level Architecture](#high-level-architecture)
- [Microservices Overview](#microservices-overview)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Running the System](#running-the-system)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## **High-Level Architecture**
```plaintext
                                   +---------------------------+
                                   |    Frontend (Optional)    |
                                   |      React or Angular     |
                                   +---------------------------+
                                            |
                                            v
                                   +---------------------------+
                                   |    API Gateway Service    |
                                   |  (Node.js + Express)      |
                                   +---------------------------+
                                      |                 |
                                      |                 |
                                      v                 v
                     +----------------+               +----------------+
                     | User Service   |               | Upload Service |
                     |  (NodeJS)     )|               |  (Python/Flask)|
                     +----------------+               +----------------+
                            |                                  |
                            v                                  v
                    +----------------+               +---------------------------+
                    | NoSQL Database |               |       S3 Storage          |
                    |  & Redis       |               |   (AWS S3 Buckets)        |
                    +----------------+               +---------------------------+
                                                        |
                                                        v
                              +---------------------------+
                              |       Queue System        |
                              |             RabbitMQ      |
                              +---------------------------+
                                      |
                                      v
                                   +---------------------------+
                                   |  Queue Service Go)        |
                                   +---------------------------+
```

---

## **Microservices Overview**
1. **API Gateway Service:**
   - Acts as the central entry point for all external requests.
   - Routes incoming requests to appropriate backend services.
   - Technologies: **Node.js**, **Express**.

2. **User Service:**
   - Manages user-related operations such as registration, authentication, and profile management.
   - Utilizes **NoSQL Database** for user data storage.
   - Technologies: **Python**, **Flask**, **NoSQL Database**.

3. **Upload Service:**
   - Handles file uploads and integrates with a PostgreSQL database for metadata storage.
   - Utilizes **AWS S3** for scalable file storage of large files.
   - Produces tasks into the **Queue System**.
   - Technologies: **Python**, **Flask**, **PostgreSQL**, **AWS S3**.

4. **Consumer Service:**
   - Processes tasks from the **Queue System**.
   - Consumes files from **AWS S3** and fetches user data from the **NoSQL Database**.
   - Technologies: **Python**, **AWS S3**, **NoSQL Database**, **RabbitMQ**.

5. **Queue System:**
   - Manages task queues and asynchronous processing using RabbitMQ.
   - Serves as the intermediary between **Upload Service** (producer) and **Consumer Service**.
   - Technologies: **Go**, **RabbitMQ**.

6. **S3 Storage:**
   - Handles scalable file storage using AWS S3 buckets for large files or backups.
   - Used by **Upload Service** and **Consumer Service**.
   - Technologies: **AWS S3**.

7. **NoSQL Database:**
   - Stores user data for the **User Service**.
   - Technologies: **NoSQL Database**.

---

## **Technologies Used**
- **Frontend (Optional):** React or Angular.
- **Backend:**
  - API Gateway: Node.js + Express.
  - User Service: Python + Flask.
  - Upload Service: Python + Flask.
  - Consumer Service: Python.
- **Queue System:** Go + RabbitMQ.
- **Storage:** AWS S3 (Used by Upload Service and Consumer Service).
- **Database:** NoSQL (Used by User Service).
- **Messaging Queue:** RabbitMQ.
- **Containerization:** Docker & Docker Compose.

---

## **Setup Instructions**

### **Prerequisites**
- **Docker**: Install [Docker](https://www.docker.com/).
- **Docker Compose**: Included with Docker Desktop.
- **Node.js**: If running the API Gateway locally.
- **Python**: Required for Python-based services.
- **Go**: Required for the Queue System.
- **heroku Account**: For S3 setup.

### **Running the System**
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Start Services with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

## **Contributing**

We welcome contributions! Follow these steps to get involved:

1. **Fork the repository**:
   Create a personal copy of the repository on GitHub.

2. **Create a feature branch**:
   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes and commit them**:
   ```bash
   git commit -m "Add feature description"
   ```

4. **Push your changes to GitHub**:
   ```bash
   git push origin feature-name
   ```

5. **Submit a pull request**:
   Open a pull request in the main repository for review.

---

## **License**

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## **Contact**

For questions or support, feel free to contact the maintainers:

- **Muhammad Hamza Sohail**
- **Idrak Islam**

