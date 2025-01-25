# **CelAI Backend**

This repository contains a collection of microservices designed to work together as a distributed system. Each microservice is responsible for specific functionality and communicates with others through the **API Gateway** or message queues.

---

Project Overview
Microservices
api_gateway_service:
Acts as the central entry point for all external requests. Routes requests to appropriate backend services and ensures proper communication between services.

queue_service:
Handles messaging and task queues, enabling asynchronous processing and inter-service communication via RabbitMQ.

upload_service:
Manages file uploads and processes them. Integrates with the database for storage and provides APIs for managing uploaded content.

user_service:
Responsible for user management, including registration, authentication, and user profile operations.

Architecture
The system is built using microservices architecture to ensure modularity, scalability, and maintainability.
Each service is deployed independently and communicates via HTTP or message queues.
Technologies Used
API Gateway: Node.js + Express
Queue Service: Go + RabbitMQ
Upload Service: Python + Flask
User Service: Python + Flask
Database: PostgreSQL (for persistent storage)
Messaging: RabbitMQ (for inter-service communication)
Setup Instructions
Requirements
Docker & Docker Compose: To containerize and manage services.
Node.js (if running locally): Required for api_gateway_service.
Python (if running locally): Required for Python-based services.
Go (if running locally): Required for queue_service.
Local Development
Clone the Repository:

bash
Copy
Edit
git clone <repository-url>
cd <repository-folder>
Start Services with Docker Compose:

bash
Copy
Edit
docker-compose up --build
Access Services:

API Gateway: http://localhost:8080
RabbitMQ Management: http://localhost:15672 (default username/password: guest/guest)
Contributing
Fork the repository
Clone a copy of this repository into your GitHub account.

Create a feature branch
Create a new branch for your feature or bugfix:

bash
Copy
Edit
git checkout -b feature-name
Commit your changes
Add a commit message describing your changes:

bash
Copy
Edit
git commit -m "Add feature description"
Push to the branch
Push your changes to your fork:

bash
Copy
Edit
git push origin feature-name
Create a pull request
Open a pull request in the main repository for review.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, feel free to contact the maintainers:

Muhammad Hamza Sohail
Idrak Islam

## **High-Level Architecture Diagram (Using Dotted Lines)**
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
