#!/usr/bin/env python3
"""
Test only Java execution to verify the fix
"""
import requests
import json

def test_java():
    """Test Java execution specifically"""
    print("Testing Java execution fix...")
    
    test_cases = [
        {
            "name": "Java - Hello World",
            "code": """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}
""".strip()
        },
        {
            "name": "Java - Math Operations",
            "code": """
public class Main {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        double average = (double) sum / numbers.length;
        
        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);
    }
}
""".strip()
        },
        {
            "name": "Java - String Operations",
            "code": """
public class Main {
    public static void main(String[] args) {
        String message = "Java Programming";
        String[] words = message.split(" ");
        
        System.out.println("Original: " + message);
        System.out.println("Length: " + message.length());
        System.out.println("Uppercase: " + message.toUpperCase());
        System.out.println("Word count: " + words.length);
    }
}
""".strip()
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {test_case['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                "http://localhost:5002/api/execute/direct",
                json={
                    "code": test_case["code"],
                    "language": "java"
                },
                timeout=30
            )
            
            result = response.json()
            print(f"Status: {result.get('status')}")
            
            if result.get("status") == "success":
                print("✅ SUCCESS")
                print(f"Output:\n{result.get('output')}")
                print(f"Execution Time: {result.get('execution_time', 0):.3f}s")
                passed += 1
            else:
                print("❌ FAILED")
                print(f"Error: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ REQUEST FAILED: {e}")
    
    print(f"\n{'='*50}")
    print("JAVA TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All Java tests passed!")
        return True
    else:
        print("⚠️ Some Java tests failed.")
        return False

if __name__ == "__main__":
    test_java()
