#!/usr/bin/env python3
"""
Debug the exact execution commands
"""
import subprocess
import base64

def test_container_commands():
    """Test the exact commands we're running in the container"""
    container_name = "leetcodecompiler-python-1"
    
    print("Testing container execution commands...")
    print("=" * 60)
    
    # Test 1: Check current working directory
    print("\n1. Check current working directory:")
    result = subprocess.run(
        ["docker", "exec", container_name, "pwd"],
        capture_output=True, text=True
    )
    print(f"PWD: {result.stdout.strip()}")
    
    # Test 2: Check if we can write to current directory
    print("\n2. Test write to current directory:")
    result = subprocess.run(
        ["docker", "exec", container_name, "touch", "test_file.txt"],
        capture_output=True, text=True
    )
    print(f"Touch result: {result.returncode}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    # Test 3: Check /tmp permissions
    print("\n3. Check /tmp permissions:")
    result = subprocess.run(
        ["docker", "exec", container_name, "ls", "-la", "/tmp"],
        capture_output=True, text=True
    )
    print(f"Tmp listing:\n{result.stdout}")
    
    # Test 4: Test base64 command
    print("\n4. Test base64 command:")
    test_code = "print('Hello World')"
    encoded_code = base64.b64encode(test_code.encode('utf-8')).decode('ascii')
    print(f"Encoded code: {encoded_code}")
    
    result = subprocess.run(
        ["docker", "exec", container_name, "sh", "-c", f"echo '{encoded_code}' | base64 -d"],
        capture_output=True, text=True
    )
    print(f"Base64 decode result: {result.returncode}")
    print(f"Decoded output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    # Test 5: Test file creation in /tmp
    print("\n5. Test file creation in /tmp:")
    result = subprocess.run(
        ["docker", "exec", container_name, "sh", "-c", f"echo '{encoded_code}' | base64 -d > /tmp/test_script.py"],
        capture_output=True, text=True
    )
    print(f"File creation result: {result.returncode}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    # Test 6: Check if file was created
    print("\n6. Check if file was created:")
    result = subprocess.run(
        ["docker", "exec", container_name, "ls", "-la", "/tmp/test_script.py"],
        capture_output=True, text=True
    )
    print(f"File check result: {result.returncode}")
    print(f"File info: {result.stdout}")
    
    # Test 7: Try to run the file
    print("\n7. Try to run the file:")
    result = subprocess.run(
        ["docker", "exec", container_name, "python3", "/tmp/test_script.py"],
        capture_output=True, text=True
    )
    print(f"Execution result: {result.returncode}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    # Test 8: Clean up
    print("\n8. Clean up:")
    subprocess.run(
        ["docker", "exec", container_name, "rm", "-f", "/tmp/test_script.py", "test_file.txt"],
        capture_output=True, text=True
    )
    print("Cleanup completed")

if __name__ == "__main__":
    test_container_commands()
