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
                                   |      NextJS               |
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

## **Microservices Overview (Infra @ Heroku)**

1. **API Gateway Service:**  
   - Central entry point for all external requests.  
   - Routes incoming requests to appropriate backend services.  
   - Technologies: **Node.js**, **Express**  

2. **User Service:**  
   - Manages user operations: registration, authentication, profile management.  
   - Stores user data in **Cloud Firestore**.  
   - Technologies: **Python**, **Flask**, **Cloud Firestore**  

3. **Upload Service:**  
   - Handles file uploads and metadata storage.  
   - Uses **Heroku Storage Add-ons (S3-compatible)** for scalable file storage.  
   - Produces tasks into the **Queue System**.  
   - Technologies: **Python**, **Flask**, **Heroku Storage**, **Cloud Firestore**  

4. **Consumer Service:**  
   - Processes tasks from the **Queue System**.  
   - Consumes files from **Heroku Storage** and fetches user data from **Cloud Firestore**.  
   - Technologies: **Python**, **Heroku Storage**, **Cloud Firestore**, **RabbitMQ**  

5. **Queue System:**  
   - Manages task queues and asynchronous processing using **RabbitMQ**.  
   - Acts as the intermediary between **Upload Service** (producer) and **Consumer Service**.  
   - Technologies: **Go**, **RabbitMQ**  

6. **Storage:**  
   - Handles scalable file storage for uploads/backups via **Heroku Storage Add-ons**.  
   - Used by **Upload Service** and **Consumer Service**.  

7. **Database:**  
   - Stores user and service metadata.  
   - Powered by **Cloud Firestore**  

---

## **Technologies Used**
- **Frontend:** **Next.js**  
- **Backend:** Node.js + Express (API Gateway), Python + Flask (User & Upload Service), Python (Consumer Service)  
- **Queue System:** Go + RabbitMQ  
- **Storage:** Heroku Storage Add-ons (S3-compatible)  
- **Database:** Cloud Firestore  
- **Messaging Queue:** RabbitMQ  
- **Containerization:** Docker & Docker Compose  

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

