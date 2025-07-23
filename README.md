# LeetCode Compiler

A simplified code execution service that supports Python, JavaScript, C++, and Java.

## Features

- Execute code in isolated Docker containers
- Support for multiple programming languages
- Redis-based job queue for scalability
- RESTful API with health checks
- Direct execution mode for testing

## Quick Start

1. **Start the services:**
   \`\`\`bash
   docker-compose up -d
   \`\`\`

2. **Test the API:**
   \`\`\`bash
   python test_api.py
   \`\`\`

3. **Execute code directly:**
   \`\`\`bash
   curl -X POST http://localhost:5002/api/execute/direct \
     -H "Content-Type: application/json" \
     -d '{"code": "print(\"Hello World!\")", "language": "python"}'
   \`\`\`

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/execute` - Queue code execution
- `GET /api/job/<job_id>` - Get job status
- `POST /api/execute/direct` - Direct execution (no queue)

## Supported Languages

- **Python** - `.py` files
- **JavaScript** - `.js` files  
- **C++** - `.cpp` files
- **Java** - `.java` files (Main class required)

## Example Request

\`\`\`json
{
  "code": "print('Hello World!')",
  "language": "python"
}
\`\`\`

## Example Response

\`\`\`json
{
  "status": "success",
  "output": "Hello World!",
  "error": null,
  "execution_time": 0.123,
  "execution_id": "uuid-here"
}
\`\`\`

## Development

- API runs on port 5002
- Redis runs on port 6379
- Logs are available via `docker-compose logs`

## Troubleshooting

1. **Container issues:** `docker-compose down && docker-compose up -d`
2. **Permission issues:** Ensure Docker socket is accessible
3. **Port conflicts:** Check if ports 5002/6379 are available
