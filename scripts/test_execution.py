#!/usr/bin/env python3
"""
Test the updated execution logic
"""
import requests
import json

def test_direct_execution():
    """Test the updated direct execution"""
    print("Testing updated execution logic...")
    
    test_cases = [
        {
            "name": "Python Hello World",
            "code": "print('Hello from Python!')",
            "language": "python"
        },
        {
            "name": "Python Math",
            "code": "print(f'2 + 2 = {2 + 2}')\nprint(f'10 * 5 = {10 * 5}')",
            "language": "python"
        },
        {
            "name": "Python with Special Characters",
            "code": "print('Hello \"World\"!')\nprint(\"It's working!\")",
            "language": "python"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {test_case['name']}")
        print(f"Code:\n{test_case['code']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                "http://localhost:5002/api/execute/direct",
                json={
                    "code": test_case["code"],
                    "language": test_case["language"]
                },
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if result.get("status") == "success":
                print("✅ SUCCESS")
            else:
                print("❌ FAILED")
                
        except Exception as e:
            print(f"❌ REQUEST FAILED: {e}")

if __name__ == "__main__":
    test_direct_execution()
