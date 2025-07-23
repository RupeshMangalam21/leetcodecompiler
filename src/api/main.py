from flask import Flask, request, jsonify
import sys
import os
sys.path.append('/app/src')

# Clear any cached imports
if 'api.execution' in sys.modules:
    del sys.modules['api.execution']

from api.execution import main
from db.models import SessionLocal, User
from rq import Queue
from redis import Redis

app = Flask(__name__)

# Redis connection with error handling
try:
    r = Redis(host='redis', port=6379)
    r.ping()  # Test connection
    q = Queue(connection=r)
    print("Successfully connected to Redis")
except Exception as e:
    print(f"Redis connection failed: {e}")
    r = None
    q = None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "LeetCode Compiler API",
        "version": "1.0",
        "supported_languages": ["python", "nodejs", "cpp", "java"]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    redis_status = "connected" if r else "disconnected"
    return jsonify({
        "status": "ok",
        "redis": redis_status
    }), 200

@app.route('/api/execute', methods=['POST'])
def execute_code_endpoint():
    data = request.get_json()
    code = data.get("code")
    language = data.get("language")
    
    if not code or not language:
        return jsonify({"status": "failure", "error": "Code and language are required"}), 400

    try:
        if q:
            # Enqueue the task for the worker
            job_id = enqueue_code_execution(language, code)
            return jsonify({"status": "success", "job_id": job_id}), 200
        else:
            # Fallback to direct execution if Redis is unavailable
            result = main(code, language)
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500

@app.route('/api/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    if not q:
        return jsonify({"error": "Queue service unavailable"}), 503
        
    try:
        job = q.fetch_job(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404

        if job.is_finished:
            return jsonify({
                "status": "completed",
                "result": job.result
            }), 200
        elif job.is_failed:
            return jsonify({
                "status": "failed",
                "error": str(job.exc_info) if job.exc_info else "Job execution failed"
            }), 200
        else:
            return jsonify({"status": "pending"}), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/execute/direct', methods=['POST'])
def execute_direct():
    """Direct execution without queue (for testing)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        code = data.get("code", "").strip()
        language = data.get("language", "").lower()
        
        if not code or not language:
            return jsonify({"error": "Code and language are required"}), 400
            
        print(f"Direct execution request: language={language}, code_length={len(code)}")
        result = main(code, language)
        print(f"Direct execution result: {result}")
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Direct execution error: {e}")
        return jsonify({"error": str(e)}), 500

def enqueue_code_execution(language, code):
    """Enqueues code execution task and returns job ID."""
    job = q.enqueue(main, code, language, timeout=60)
    return job.get_id()

if __name__ == '__main__':
    print("Starting LeetCode Compiler API...")
    print("Clearing Python cache...")
    # Clear cache on startup
    import subprocess
    try:
        subprocess.run(["find", "/app", "-name", "__pycache__", "-type", "d", "-exec", "rm", "-rf", "{}", "+"], 
                      capture_output=True)
        subprocess.run(["find", "/app", "-name", "*.pyc", "-delete"], capture_output=True)
    except:
        pass
    
    app.run(host='0.0.0.0', port=7000, debug=True)
