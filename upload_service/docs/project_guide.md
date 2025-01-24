# Documentation for Flask App with S3 and RabbitMQ

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)
- [License](#license)

---

## Project Structure
```plaintext
.
├── app.py                 # Main application code
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── Makefile               # Commands for setup, testing, and running
├── .env                   # Environment variables
├── tests/                 # Test cases for the application
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci_cd_pipeline.yml  # CI/CD pipeline configuration
├── README.md              # Project documentation
```

---

## Setup and Installation
### Prerequisites
- Python 3.10 or higher
- Docker (optional for containerized deployment)
- RabbitMQ server
- AWS credentials for S3

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url.git
   cd your-repo-folder
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables
Create a `.env` file in the project root with the following values:
```plaintext
# AWS S3 Configuration
S3_ENDPOINT_URL=https://your-s3-endpoint.com
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION_NAME=us-east-1
S3_BUCKET_NAME=your-bucket-name

# RabbitMQ Configuration
RABBITMQ_URL=amqps://user:password@your-rabbitmq-url
RABBITMQ_QUEUE_NAME=metadata_queue
```

---

## Running the Application
### Local Development
1. Set Flask environment variables:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```

2. Run the application:
   ```bash
   flask run
   ```

The app will be available at `http://127.0.0.1:5000`.

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t flask-app .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 --env-file .env flask-app
   ```

---

## Testing
Run tests using `pytest`:
```bash
make test
```
This will execute all test cases located in the `tests/` directory.

---

## CI/CD Pipeline
The project uses GitHub Actions for CI/CD. The pipeline:
- Installs dependencies.
- Runs tests on push or pull request events (if enabled).

### Manually Triggering the Pipeline
1. Go to the **Actions** tab in your GitHub repository.
2. Select the workflow **Test Pipeline**.
3. Click **Run workflow**.

---

## Contributing
### Guidelines
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your message"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Submit a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

