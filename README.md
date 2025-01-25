# **CelAI Backend**

This repository contains a collection of microservices designed to work together as a distributed system. Each microservice is responsible for a specific functionality and communicates with others through the **API Gateway** or message queues.

---

### **High-Level Architecture Diagram (Using Dotted Lines)**
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

## **Project Overview**

### **Microservices**
1. **`api_gateway_service`:**  
   Acts as the central entry point for all external requests. Routes requests to appropriate backend services and ensures proper communication between services.

2. **`queue_service`:**  
   Handles messaging and task queues, enabling asynchronous processing and inter-service communication via RabbitMQ.

3. **`upload_service`:**  
   Manages file uploads and processes them. Integrates with the database for storage and provides APIs for managing uploaded content.

4. **`user_service`:**  
   Responsible for user management, including registration, authentication, and user profile operations.

---

## **Architecture**
- The system is built using microservices architecture to ensure modularity, scalability, and maintainability.
- Each service is deployed independently and communicates via HTTP or message queues.

### **Technologies Used**
- **API Gateway:** Node.js + Express
- **Queue Service:** Go + RabbitMQ
- **Upload Service:** Python + Flask
- **User Service:** Python + Flask
- **Database:** PostgreSQL (for persistent storage)
- **Messaging:** RabbitMQ (for inter-service communication)

---

## **Setup Instructions**

### **Requirements**
- **Docker & Docker Compose:** To containerize and manage services.
- **Node.js (if running locally):** Required for `api_gateway_service`.
- **Python (if running locally):** Required for Python-based services.
- **Go (if running locally):** Required for `queue_service`.

---

### **Local Development**
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>

## **Contributing**

1. **Fork the repository**  
   Clone a copy of this repository into your GitHub account.

2. **Create a feature branch**  
   Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, feel free to contact the maintainers:

Muhammad Hamza Sohail
Idrak Islam
