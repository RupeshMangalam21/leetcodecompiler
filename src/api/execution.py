import subprocess
import time
import logging
import uuid
import base64
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_code_simple(code: str, language: str) -> Dict[str, Any]:
    """
    Simplified code execution that works directly in /tmp
    """
    execution_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Validate language
        supported_languages = ["python", "nodejs", "cpp", "java"]
        if language not in supported_languages:
            return {
                "status": "failure", 
                "error": f"Unsupported language: {language}. Supported: {supported_languages}",
                "execution_id": execution_id
            }

        # Container mapping
        container_map = {
            "python": "leetcodecompiler-python-1",
            "nodejs": "leetcodecompiler-node-1", 
            "cpp": "leetcodecompiler-cpp-1",
            "java": "leetcodecompiler-java-1"
        }

        container_name = container_map.get(language)
        if not container_name:
            return {"status": "failure", "error": f"No container for language: {language}"}

        logger.info(f"Executing code: id={execution_id}, language={language}, container={container_name}")

        # Use base64 encoding to safely transfer code
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('ascii')
        
        # Create unique filename in /tmp
        script_name = f"script_{execution_id}"
        
        # Build execution command based on language - work directly in /tmp
        if language == "java":
            # Java requires the filename to match the public class name
            # For simplicity, we'll always use "Main.java" and expect the class to be named "Main"
            command = [
                "docker", "exec", container_name,
                "sh", "-c", 
                f"cd /tmp && echo '{encoded_code}' | base64 -d > Main.java && javac Main.java && java Main"
            ]
        elif language == "cpp":
            command = [
                "docker", "exec", container_name,
                "sh", "-c", 
                f"cd /tmp && echo '{encoded_code}' | base64 -d > {script_name}.cpp && g++ -o {script_name} {script_name}.cpp && ./{script_name}"
            ]
        elif language == "nodejs":
            command = [
                "docker", "exec", container_name,
                "sh", "-c", 
                f"cd /tmp && echo '{encoded_code}' | base64 -d > {script_name}.js && node {script_name}.js"
            ]
        else:  # python
            command = [
                "docker", "exec", container_name,
                "sh", "-c", 
                f"cd /tmp && echo '{encoded_code}' | base64 -d > {script_name}.py && python3 {script_name}.py"
            ]

        logger.info(f"Executing command: {' '.join(command)}")

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )

        execution_time = time.time() - start_time
        response = {
            "status": "success" if result.returncode == 0 else "failure",
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None,
            "execution_time": execution_time,
            "execution_id": execution_id,
            "container_used": container_name
        }

        # Cleanup
        try:
            if language == "java":
                # Clean up Java files (source and class files)
                subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", "cd /tmp && rm -f Main.java Main.class"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
            else:
                subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", f"cd /tmp && rm -f {script_name}.*"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
        except:
            pass  # Ignore cleanup errors

        logger.info(f"Execution completed: id={execution_id}, status={response['status']}")
        return response

    except subprocess.TimeoutExpired:
        logger.error(f"Code execution timed out: id={execution_id}")
        return {"status": "timeout", "error": "Execution timed out", "execution_id": execution_id}

    except Exception as e:
        logger.error(f"Execution failed: id={execution_id}", exc_info=True)
        return {"status": "error", "error": str(e), "execution_id": execution_id}

def main(code: str, language: str) -> Dict[str, Any]:
    """Main execution interface"""
    return execute_code_simple(code, language)
