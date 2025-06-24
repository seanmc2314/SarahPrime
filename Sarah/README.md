# Sarah AI Web Application

A web application for an AI agent named Sarah that connects to OpenAI's 
API, allows chatting, and supports self-growth with a guardian feature. 
Uses Flask for the backend and React with Tailwind CSS for the frontend.

## Setup

1. **Prerequisites**:
   - Python 3.9+, Node.js 18+, Docker, Git.
   - OpenAI API key from https://platform.openai.com/account/api-keys.

2. **Backend**:
   - Copy `backend/.env.example` to `backend/.env` and add your API key.
   - Install dependencies:
     ```bash
     cd backend
     pip install -r requirements.txt
