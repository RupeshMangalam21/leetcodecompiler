#!/usr/bin/env python3
"""
Debug script to check container permissions and setup
"""
import subprocess
import json

def run_docker_command(container_name, command, description):
    """Run a command in the specified container"""
    print(f"\n{description}:")
    print("-" * 50)
    try:
        result = subprocess.run(
            ["docker", "exec", container_name] + command,
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"Command: {' '.join(command)}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Error:\n{result.stderr}")
    except Exception as e:
        print(f"Failed to run command: {e}")

def main():
    container_name = "leetcodecompiler-python-1"
    
    print(f"Debugging container: {container_name}")
    print("=" * 60)
    
    # Check if container is running
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        if container_name not in result.stdout:
            print(f"Container {container_name} is not running!")
            return
    except Exception as e:
        print(f"Failed to check container status: {e}")
        return
    
    # Debug commands
    debug_commands = [
        (["whoami"], "Current user"),
        (["id"], "User ID and groups"),
        (["pwd"], "Current working directory"),
        (["ls", "-la", "/"], "Root directory permissions"),
        (["ls", "-la", "/tmp"], "Tmp directory permissions"),
        (["ls", "-la", "/leetcode_compiler"], "Leetcode compiler directory permissions"),
        (["touch", "/tmp/test.txt"], "Test write to /tmp"),
        (["ls", "-la", "/tmp/test.txt"], "Check created test file"),
        (["rm", "/tmp/test.txt"], "Clean up test file"),
        (["mkdir", "-p", "/tmp/workspace"], "Create workspace directory"),
        (["ls", "-la", "/tmp/workspace"], "Check workspace permissions"),
    ]
    
    for command, description in debug_commands:
        run_docker_command(container_name, command, description)

if __name__ == "__main__":
    main()
