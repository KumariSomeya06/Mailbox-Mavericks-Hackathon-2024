# FastAPI GPT-4 Email Responder

This project is a FastAPI-based application designed to access and generate response emails using GPT-4. The project includes guidelines for setting up the environment and managing sensitive data securely.

## Features
- Generate professional email responses using GPT-4.
- Easy-to-use API for email-related operations.
- Environment configuration for sensitive data.

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine:
git clone <repository_url>
cd <repository_folder>

### Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

### Install Dependencies
pip install -r requirements.txt

### Configure the Environment Variables
GPT_API_KEY = "api key here"

CLIENT_ID = "client id here"
CLIENT_SECRET = "client secret key here"
TENANT_ID = "tenant id here"

USER_EMAIL = "user email here"

### Run the Application
uvicorn main:app --reload
