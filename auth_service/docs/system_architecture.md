# System Architecture of Authentication Service Microservice

## Overview
The **Authentication Service microservice** is designed to handle user authentication via **Firebase Authentication**. It allows for:
- **User sign-up**
- **User sign-in**
- **Token validation** using Firebase ID tokens

This service is built with **Node.js**, **Express.js**, and **Firebase Admin SDK**. The system architecture focuses on scalability, security, and simplicity.

---

## Key Components

### 1. **Firebase Authentication**
   - **Firebase Authentication** is responsible for managing user authentication. It supports various authentication methods, including **email/password** and **Google Sign-In**.
   - Once a user is authenticated, Firebase generates a **Firebase ID token** that can be used to identify the user securely.

### 2. **Express.js**
   - The service is built using **Express.js**, a fast, minimal web framework for Node.js. It is used to handle HTTP requests (such as sign-up, sign-in, and token validation).
   - Express handles incoming requests, processes them, and sends back the appropriate responses.

### 3. **Firebase Admin SDK**
   - The **Firebase Admin SDK** is used to verify the authenticity of the Firebase ID token that is passed from the client.
   - It is initialized with a **service account key** that allows the backend to securely interact with Firebase services.
   - The Admin SDK validates the token, retrieves the user information, and ensures the integrity and security of the authentication process.

---

## High-Level Flow

### 1. **User Registration and Sign-In**
   - The client (e.g., web or mobile app) uses Firebase Authentication to authenticate users via email/password or Google Sign-In.
   - Upon successful sign-in, Firebase generates a **Firebase ID token** for the user.

### 2. **Token Validation**
   - The client sends the **Firebase ID token** to the backend service (via the `/validate-token` endpoint).
   - The backend uses the **Firebase Admin SDK** to verify the token's validity.
   - If the token is valid, the backend responds with the **user ID** and any other relevant user data.
   - If the token is invalid or expired, the backend returns an error message.

---

## System Flow Diagram

```plaintext
Client Side (Web/Mobile)
   |
   | -> SignUp/SignIn -> Firebase Authentication -> Firebase ID Token
   |
Backend (Express.js Server)
   |
   | -> /validate-token (receives Firebase ID Token)
   |    -> Firebase Admin SDK (Verify Token)
   |
   | -> Return user ID or error



## Detailed Architecture

### Client-Side:
- The client interacts with **Firebase Authentication** for user sign-up/sign-in.
- After authentication, Firebase generates a **Firebase ID token** that is sent to the backend.

### Backend (Express.js):
- The backend receives the **Firebase ID token** from the client.
- It uses the **Firebase Admin SDK** to validate the token.
- The backend responds with the **user ID** if the token is valid, or an error if the token is invalid.

### Firebase Admin SDK:
- The **Firebase Admin SDK** verifies the integrity of the Firebase ID token by decoding and checking its signature.
- It ensures that the token has not expired and that it was issued by the correct Firebase project.

---

## Security Considerations

### JWT-Based Authentication:
- Firebase ID tokens are **JWT tokens**, which ensures that they are secure and tamper-proof. The signature of the token can only be verified with the correct Firebase project credentials.

### Short-Lived Tokens:
- Firebase ID tokens are valid for **1 hour**. This reduces the risk of long-lived tokens being compromised. The client can refresh the token when necessary.

### Service Account Key:
- The **Firebase Admin SDK** is initialized using a **service account key**, ensuring that the backend can securely communicate with Firebase services.

---

## Future Enhancements

### OAuth Integration:
- Integrate additional OAuth providers for more sign-in options (e.g., **GitHub**, **Facebook**).

### Rate Limiting:
- Implement **rate limiting** to prevent abuse of authentication endpoints.

### Token Refresh Endpoint:
- Add a dedicated endpoint to **refresh Firebase ID tokens** using Firebase's built-in functionality.
