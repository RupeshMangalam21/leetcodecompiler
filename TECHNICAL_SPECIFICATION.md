# LeetCode Compiler - Technical Specification

## Overview

The LeetCode Compiler is a distributed code execution service designed to safely execute user-submitted code in multiple programming languages within isolated Docker containers. The system provides a RESTful API for code submission, uses Redis for job queuing, and PostgreSQL for data persistence.

## Architecture

### System Components

\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client/UI     │───▶│   Flask API     │───▶│   Redis Queue   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   RQ Worker     │
                       │   Database      │    │   Process       │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                              ┌─────────────────┐
                                              │ Docker Language │
                                              │   Containers    │
                                              └─────────────────┘
\`\`\`

### Core Services

#### 1. Flask API Server (`src/api/main.py`)
- **Purpose**: HTTP REST API endpoint for code execution requests
- **Port**: 7000 (exposed as 5002)
- **Responsibilities**:
  - Request validation and sanitization
  - Job queuing via Redis
  - Health monitoring
  - Direct execution fallback
- **Key Endpoints**:
  - `GET /` - API information
  - `GET /health` - System health check
  - `POST /api/execute` - Queue code execution
  - `GET /api/job/<job_id>` - Job status polling
  - `POST /api/execute/direct` - Synchronous execution

#### 2. Redis Queue System
- **Purpose**: Asynchronous job processing and result caching
- **Port**: 6379
- **Features**:
  - Job persistence with Redis RDB
  - Automatic job timeout (60 seconds)
  - Job status tracking (pending/completed/failed)

#### 3. RQ Worker Process (`src/api/worker.py`)
- **Purpose**: Background job execution
- **Responsibilities**:
  - Dequeue jobs from Redis
  - Execute code via Docker containers
  - Return results to Redis
  - Error handling and logging

#### 4. PostgreSQL Database
- **Purpose**: User management and execution history
- **Port**: 5432
- **Schema**: User authentication and session management

#### 5. Language-Specific Docker Containers
- **Purpose**: Isolated code execution environments
- **Security**: Non-root execution, resource limits, capability dropping

## Language Support

### Supported Languages

| Language   | File Extension | Container Base Image | Execution Method   |
|------------|----------------|----------------------|--------------------|
| Python     | `.py`          | `python:3.9-slim`    | `python3 script.py`|
| JavaScript | `.js`          | `node:16-slim`       | `node script.js`   |
| C++        | `.cpp`         | `gcc:latest`         | Compile + Execute  |
| Java       | `.java`        | `openjdk:17-jdk-slim`| Compile + Execute  |

### Execution Flow

1. **Code Submission**: Client submits code via REST API
2. **Validation**: API validates language support and code presence
3. **Job Creation**: Job queued in Redis with unique execution ID
4. **Worker Processing**: RQ worker dequeues job
5. **Container Execution**: Code executed in isolated Docker container
6. **Result Collection**: Output/errors captured and returned
7. **Cleanup**: Temporary files and resources cleaned up

## Security Architecture

### Container Security
- **User Isolation**: Non-root user execution (`executor` user)
- **Resource Limits**: 
  - Memory: 512MB per container
  - CPU: 1 core limit
  - Process limit: 50 PIDs
- **Security Options**:
  - `--security-opt=no-new-privileges`
  - `--cap-drop=ALL`
  - Read-only filesystem where possible

### Java-Specific Security
- **Security Policy**: Custom `java.policy` file
- **Permissions**:
  - File read access limited to `/app/` directory
  - Standard I/O permissions
  - Property read permissions only

### Network Security
- **Container Isolation**: No network access for execution containers
- **Internal Communication**: Services communicate via Docker network
- **Port Exposure**: Only API port exposed to host

## Data Flow

### Synchronous Execution (Direct)
\`\`\`
Client Request → API Validation → Docker Execution → Response
\`\`\`

### Asynchronous Execution (Queued)
\`\`\`
Client Request → API Validation → Redis Queue → Job ID Response
                                      ↓
Worker Process → Docker Execution → Result Storage → Client Polling
\`\`\`

## Error Handling

### Error Categories
1. **Validation Errors**: Invalid language, missing code
2. **Execution Errors**: Compilation failures, runtime exceptions
3. **Timeout Errors**: 30-second execution limit
4. **System Errors**: Container failures, resource exhaustion

### Error Response Format
\`\`\`json
{
  "status": "error|timeout|failure",
  "error": "Error description",
  "execution_id": "uuid",
  "execution_time": 0.0
}
\`\`\`

## Performance Characteristics

### Execution Limits
- **Timeout**: 30 seconds per execution
- **Memory**: 512MB per container
- **CPU**: 1 core per execution
- **Concurrent Jobs**: Limited by worker processes

### Scalability
- **Horizontal Scaling**: Multiple worker processes
- **Container Reuse**: Long-running containers for efficiency
- **Queue Management**: Redis handles job distribution

## Monitoring and Logging

### Health Checks
- API health endpoint (`/health`)
- Redis connectivity monitoring
- Container status verification

### Logging
- Structured logging with execution IDs
- Error tracking with stack traces
- Performance metrics (execution time)

## Technology Stack

### Backend
- **Python 3.11**: Core application language
- **Flask 2.3.3**: Web framework
- **SQLAlchemy 2.0.23**: ORM for database operations
- **RQ 1.15.1**: Redis-based job queue
- **Redis 4.6.0**: In-memory data store

### Infrastructure
- **Docker**: Container orchestration
- **Docker Compose**: Multi-service deployment
- **PostgreSQL 13**: Relational database
- **Redis 6.2**: Job queue and caching

### Security
- **Docker Security**: Container isolation and resource limits
- **Java Security Manager**: Policy-based execution control
- **Non-root Execution**: All containers run as non-privileged users

## API Specification

### Request Format
\`\`\`json
{
  "code": "print('Hello World')",
  "language": "python"
}
\`\`\`

### Response Format
\`\`\`json
{
  "status": "success",
  "output": "Hello World",
  "error": null,
  "execution_time": 0.123,
  "execution_id": "550e8400-e29b-41d4-a716-446655440000"
}
\`\`\`

### HTTP Status Codes
- `200`: Successful execution
- `202`: Job queued successfully
- `400`: Invalid request
- `404`: Job not found
- `500`: Internal server error
- `503`: Service unavailable

## File Structure

\`\`\`
leetcode-compiler/
├── src/
│   ├── api/
│   │   ├── main.py          # Flask API server
│   │   ├── worker.py        # RQ worker process
│   │   └── execution.py     # Code execution service
│   └── db/
│       └── models.py        # Database models
├── docker/
│   ├── cpp/                 # C++ execution environment
│   ├── java/                # Java execution environment
│   ├── nodejs/              # Node.js execution environment
│   └── python/              # Python execution environment
├── docker-compose.yml       # Service orchestration
├── Dockerfile              # API server image
├── Dockerfile.worker       # Worker process image
└── requirements.txt        # Python dependencies
