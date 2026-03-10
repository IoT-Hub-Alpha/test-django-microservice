# FastAPI Project Setup Instructions for Claude Code

Use these instructions to generate the same microservice project structure but with FastAPI instead of Django.

## Project Setup

### 1. Create Virtual Environment with Python 3.13
```bash
python3.13 -m venv venv
source venv/bin/activate
```

### 2. Install FastAPI and Dependencies
```bash
pip install fastapi uvicorn httpx python-dotenv
pip freeze > requirements.txt
```

### 3. Project Structure
Create the following structure:
```
fastapi-test-microservice/
├── venv/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── routes/
│       ├── __init__.py
│       └── pingpong.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Implementation Details

### 3.1 Main Application (app/main.py)
- Create FastAPI application instance
- Include routes from pingpong router
- Set up CORS if needed

### 3.2 Pingpong Routes (app/routes/pingpong.py)
Create two endpoints:

**Endpoint 1: POST /api/ping**
- Accepts JSON: `{"ping": "ping"}` or `{"ping": "boom"}`
- If receives "ping": return `{"message": "pong"}` with status 200
- If receives "boom": return `{"message": "i don't like \"BOOM\""}` with status 400
- Invalid input: return `{"error": "Invalid request"}` with status 400

**Endpoint 2: POST /api/start**
- Accepts JSON: `{"start": "start"}`
- When receives "start":
  1. Send POST to `http://127.0.0.1:8101/api/ping/` with `{"ping": "ping"}`
  2. Wait 3 seconds
  3. Send POST to `http://127.0.0.1:8101/api/ping/` with `{"ping": "boom"}`
  4. Return `{"message": "Requests sent successfully"}` with status 200
- Use `httpx` library for making HTTP requests

## Running the Server

### Development Server on Port 8100
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload
```

### Multiple Servers (8100 and 8101)
```bash
# Terminal 1
uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload

# Terminal 2
uvicorn app.main:app --host 0.0.0.0 --port 8101 --reload
```

## Testing Endpoints

### Test 1: Ping with "ping"
```bash
curl -X POST http://127.0.0.1:8100/api/ping/ \
  -H "Content-Type: application/json" \
  -d '{"ping": "ping"}'
```
Expected: `{"message": "pong"}` (Status 200)

### Test 2: Ping with "boom"
```bash
curl -X POST http://127.0.0.1:8100/api/ping/ \
  -H "Content-Type: application/json" \
  -d '{"ping": "boom"}'
```
Expected: `{"message": "i don't like \"BOOM\""}` (Status 400)

### Test 3: Start endpoint
```bash
curl -X POST http://127.0.0.1:8100/api/start/ \
  -H "Content-Type: application/json" \
  -d '{"start": "start"}'
```
Expected: `{"message": "Requests sent successfully"}` (Status 200)

## Docker Setup

### Dockerfile
- Base image: `python:3.13-slim`
- Install dependencies from requirements.txt
- Expose ports 8100 and 8101
- Run: `uvicorn app.main:app --host 0.0.0.0 --port 8100`

### .dockerignore
- venv/
- __pycache__/
- *.pyc
- .git
- .env
- .vscode/
- .idea/

### Build and Run
```bash
# Build
docker build -t fastapi-test-microservice .

# Run on 8100
docker run -p 8100:8100 fastapi-test-microservice

# Run on 8101
docker run -p 8101:8100 fastapi-test-microservice
```

## README.md Structure
Include:
1. Project title
2. Quick start command
3. Example curl commands for each endpoint
4. Docker setup instructions
5. Project structure overview

## Additional Features (Optional)
- Add API documentation at `/docs` (FastAPI built-in)
- Add health check endpoint at `/health`
- Add request logging
- Error handling for connection failures in start endpoint

## Key Differences from Django Version
- FastAPI is async-capable (use async/await if needed)
- Uses Pydantic for request/response models (optional but recommended)
- Simpler project structure (no manage.py, fewer boilerplate files)
- Built-in interactive API documentation at `/docs`
- Auto-generated OpenAPI schema at `/openapi.json`