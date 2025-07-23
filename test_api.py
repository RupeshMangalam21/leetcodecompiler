#!/usr/bin/env python3
"""
Test script for the LeetCode Compiler API
"""
import requests
import json
import time

API_BASE = "http://localhost:5002"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_direct_execution():
    """Test direct code execution"""
    print("Testing direct execution...")
    
    test_cases = [
        {
            "name": "Python Hello World",
            "code": "print('Hello from Python!')",
            "language": "python"
        },
        {
            "name": "JavaScript Hello World", 
            "code": "console.log('Hello from JavaScript!');",
            "language": "javascript"
        },
        {
            "name": "C++ Hello World",
            "code": '#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hello from C++!" << endl;\n    return 0;\n}',
            "language": "cpp"
        },
        {
            "name": "Java Hello World",
            "code": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java!");\n    }\n}',
            "language": "java"
        }
    ]
    
    for test_case in test_cases:
        print(f"Testing {test_case['name']}...")
        response = requests.post(
            f"{API_BASE}/api/execute/direct",
            json={
                "code": test_case["code"],
                "language": test_case["language"]
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
        print("-" * 50)

def test_queue_execution():
    """Test queued execution"""
    print("Testing queued execution...")
    
    # Submit job
    response = requests.post(
        f"{API_BASE}/api/execute",
        json={
            "code": "print('Hello from queued execution!')",
            "language": "python"
        }
    )
    
    if response.status_code == 202:
        job_data = response.json()
        job_id = job_data.get("job_id")
        print(f"Job submitted: {job_id}")
        
        # Poll for result
        for i in range(10):
            time.sleep(1)
            status_response = requests.get(f"{API_BASE}/api/job/{job_id}")
            status_data = status_response.json()
            print(f"Attempt {i+1}: {status_data.get('status')}")
            
            if status_data.get("status") in ["completed", "failed"]:
                print(f"Final result: {json.dumps(status_data, indent=2)}")
                break
    else:
        print(f"Failed to submit job: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    print("LeetCode Compiler API Test Suite")
    print("=" * 50)
    
    try:
        test_health()
        test_direct_execution()
        test_queue_execution()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the service is running on localhost:5002")
    except Exception as e:
        print(f"Test failed with error: {e}")
