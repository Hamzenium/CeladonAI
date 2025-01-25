## Prerequisites

Before getting started, ensure you have the following installed:

- **Node.js** (version 16 or later)
- **npm** (version 7 or later)
- **Firebase project** (for Firebase Admin SDK)
- **Docker** (optional, for containerization)

### Setting Up Firebase Admin SDK

1. **Create or Use an Existing Firebase Project**:
   - Go to the [Firebase Console](https://console.firebase.google.com/).
   - Either create a new Firebase project or use an existing one.

2. **Generate Service Account Key**:
   - Navigate to **Project Settings** > **Service accounts** in the Firebase Console.
   - Click **Generate new private key** and download the JSON file.
   - Rename the downloaded file to `serviceAccountKey.json` and place it in the root directory of your project.

---

## Installation Instructions

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/your-repo/auth_service.git
cd auth_service
2. Install Dependencies
In the project directory, run the following command to install required dependencies:

bash
Copy
npm install
This will install the following:

express: The web framework for handling HTTP requests.
firebase-admin: Firebase Admin SDK for verifying Firebase ID tokens.
3. Configuration
Ensure you have placed the serviceAccountKey.json file from Firebase in the root of your project.
Make sure any necessary configuration in app.js is set to use Firebase Admin SDK credentials.
4. Run the Application
Once dependencies are installed, you can start the application using:

bash
Copy
npm start
This will run the server locally on http://localhost:5000.

Usage
Endpoints
1. POST /auth/signup
Purpose: Register a new user with an email and password.
Request body:
json
Copy
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response:
json
Copy
{
  "message": "User created successfully",
  "userId": "some-unique-user-id"
}
2. POST /auth/signin
Purpose: Sign in a user with email and password.
Request body:
json
Copy
{
  "email": "user@example.com",
  "password": "securepassword"
}
Response:
json
Copy
{
  "token": "firebase-id-token"
}
3. POST /auth/validate-token
Purpose: Validate the Firebase ID token and get the user ID.
Request body:
json
Copy
{
  "token": "firebase-id-token"
}
Response:
json
Copy
{
  "valid": true,
  "userId": "user-uid"
}

Deployment
You can deploy the service locally or in Docker containers.

1. Docker Deployment:
To build and run the app inside a Docker container, use the Makefile commands:

Build the Docker image:

bash
Copy
make docker-build
Run the Docker container:

bash
Copy
make docker-run
Deploy using Docker (build and run in one command):

bash
Copy
make docker-deploy
2. Local Deployment:
To run the app locally, use the following Makefile commands:

Install dependencies:

bash
Copy
make install
Run the app:

bash
Copy
make run
Deploy locally (install, build, and run):

bash
Copy
make deploy
Testing
You can use Postman or any other API testing tool to test the endpoints.

Test the /validate-token Endpoint:
Once the client sends the Firebase ID token after sign-in, validate it using the /validate-token endpoint:

Method: POST
URL: http://localhost:5000/auth/validate-token
Body:
json
Copy
{
  "token": "firebase-id-token-here"
}