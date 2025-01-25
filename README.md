# **CelAI Backend**

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
                          |       |          |
                          |       |          |
                          v       |          v
         +----------------+       |          +----------------+
         | User Service   |       |          | Queue Service   |
         |  (Python/Flask)|       |          |  (Go + RabbitMQ)|
         +----------------+       |          +----------------+
                          |       |
                          v       |
                  +---------------------------+
                  |   Upload Service (Flask)  |
                  |   + PostgreSQL Database   |
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
   - Technologies: **Python**, **Flask**.

3. **Queue Service:**
   - Manages task queues and asynchronous processing using RabbitMQ.
   - Technologies: **Go**, **RabbitMQ**.

4. **Upload Service:**
   - Handles file uploads and integrates with a PostgreSQL database for storage and retrieval.
   - Technologies: **Python**, **Flask**, **PostgreSQL**.

---

## **Technologies Used**
- **Frontend (Optional):** React or Angular.
- **Backend:**
  - API Gateway: Node.js + Express.
  - User Service: Python + Flask.
  - Queue Service: Go + RabbitMQ.
  - Upload Service: Python + Flask.
- **Database:** PostgreSQL.
- **Messaging Queue:** RabbitMQ.
- **Containerization:** Docker & Docker Compose.

---

## **Setup Instructions**

### **Prerequisites**
- **Docker**: Install [Docker](https://www.docker.com/).
- **Docker Compose**: Included with Docker Desktop.
- **Node.js**: If running the API Gateway locally.
- **Python**: Required for Python-based services.
- **Go**: Required for the Queue Service.

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

3. **Access Services**:
   - **API Gateway:** [http://localhost:8080](http://localhost:8080)
   - **RabbitMQ Management Interface:** [http://localhost:15672](http://localhost:15672) (default credentials: guest/guest).

4. **Environment Variables**:
   Ensure `.env` files are set up for each service with the required variables:
   - **API Gateway:**
     ```env
     SERVICE_UPLOAD=http://upload_service:5000
     SERVICE_QUEUE=http://queue_service:4000
     ```
   - **Upload Service:**
     ```env
     DATABASE_URL=postgresql://postgres:password@db:5432/mydb
     ```
   - **Queue Service:**
     ```env
     RABBITMQ_URL=amqp://rabbitmq:5672
     ```

---

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

