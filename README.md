# Service-Template

python backend/manage.py runserver 0.0.0.0:8100

curl -X POST http://127.0.0.1:8100/api/ping/   -H "Content-Type: application/json"   -d '{"ping": "ping"}'

response: {"message": "pong"} staus 200

curl -X POST http://127.0.0.1:8100/api/ping/ \
  -H "Content-Type: application/json" \
  -d '{"ping": "boom"}'

Response: {"message": "i don't like \"BOOM\""} (Status 400)

docker build -t django-test-microservice .

docker run -p 8100:8100 django-test-microservice


## Endpoint: POST /api/start/

Sends requests to another service running on port 8101.

**Request:**
```json
{"start": "start"}
```

**What it does:**
1. Sends `{"ping": "ping"}` to `http://127.0.0.1:8101/api/ping/`
2. Waits 3 seconds
3. Sends `{"ping": "boom"}` to `http://127.0.0.1:8101/api/ping/`
4. Returns success response

**Example:**
```bash
curl -X POST http://127.0.0.1:8100/api/start/ \
  -H "Content-Type: application/json" \
  -d '{"start": "start"}'
```

**Response:**
```json
{"message": "Requests sent successfully"}
```
(Status 200)

## Docker Setup

### Build Docker Image
```bash
docker build -t django-test-microservice .
```

### Run Container on Port 8100
```bash
docker run -p 8100:8100 django-test-microservice
```

### Run Multiple Containers (8100 and 8101)
```bash
# Terminal 1
docker run -p 8100:8100 django-test-microservice

# Terminal 2
docker run -p 8101:8100 django-test-microservice
```

### Run with Custom Port
```bash
docker run -p 9000:8100 django-test-microservice
```

Access the service at `http://localhost:8100/api/ping/`