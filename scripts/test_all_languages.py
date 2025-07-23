#!/usr/bin/env python3
"""
Test all supported languages in the LeetCode Compiler
"""
import requests
import json
import time

def test_language(name, code, language):
    """Test a specific language"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Language: {language}")
    print(f"Code:\n{code}")
    print("-" * 40)
    
    try:
        response = requests.post(
            "http://localhost:5002/api/execute/direct",
            json={"code": code, "language": language},
            timeout=45
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if result.get("status") == "success":
            print("✅ SUCCESS")
            print(f"Output: {result.get('output')}")
            print(f"Execution Time: {result.get('execution_time', 0):.3f}s")
        else:
            print("❌ FAILED")
            print(f"Error: {result.get('error')}")
            
        print(f"Container Used: {result.get('container_used', 'N/A')}")
        return result.get("status") == "success"
        
    except Exception as e:
        print(f"❌ REQUEST FAILED: {e}")
        return False

def main():
    print("LeetCode Compiler - All Languages Test")
    print("=" * 60)
    
    test_cases = [
        # Python Tests
        {
            "name": "Python - Hello World",
            "code": "print('Hello from Python!')",
            "language": "python"
        },
        {
            "name": "Python - Math Operations",
            "code": """
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Sum of {numbers} = {total}")
print(f"Average = {total / len(numbers)}")
""".strip(),
            "language": "python"
        },
        {
            "name": "Python - Data Structures",
            "code": """
# Dictionary and list operations
data = {'name': 'Python', 'version': 3.9}
fruits = ['apple', 'banana', 'orange']

print(f"Language: {data['name']} {data['version']}")
print(f"Fruits: {', '.join(fruits)}")
print(f"First fruit: {fruits[0]}")
""".strip(),
            "language": "python"
        },
        
        # JavaScript/Node.js Tests
        {
            "name": "JavaScript - Hello World",
            "code": "console.log('Hello from JavaScript!');",
            "language": "nodejs"
        },
        {
            "name": "JavaScript - Array Operations",
            "code": """
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(x => x * 2);
const sum = numbers.reduce((a, b) => a + b, 0);

console.log('Original:', numbers);
console.log('Doubled:', doubled);
console.log('Sum:', sum);
""".strip(),
            "language": "nodejs"
        },
        {
            "name": "JavaScript - Object Operations",
            "code": """
const person = {
    name: 'JavaScript',
    age: 28,
    skills: ['web', 'server', 'mobile']
};

console.log(`Name: ${person.name}`);
console.log(`Age: ${person.age}`);
console.log(`Skills: ${person.skills.join(', ')}`);
""".strip(),
            "language": "nodejs"
        },
        
        # C++ Tests
        {
            "name": "C++ - Hello World",
            "code": """
#include <iostream>
using namespace std;

int main() {
    cout << "Hello from C++!" << endl;
    return 0;
}
""".strip(),
            "language": "cpp"
        },
        {
            "name": "C++ - Math Operations",
            "code": """
#include <iostream>
#include <vector>
#include <numeric>
using namespace std;

int main() {
    vector<int> numbers = {1, 2, 3, 4, 5};
    int sum = accumulate(numbers.begin(), numbers.end(), 0);
    
    cout << "Numbers: ";
    for(int i = 0; i < numbers.size(); i++) {
        cout << numbers[i];
        if(i < numbers.size() - 1) cout << ", ";
    }
    cout << endl;
    cout << "Sum: " << sum << endl;
    cout << "Average: " << (double)sum / numbers.size() << endl;
    
    return 0;
}
""".strip(),
            "language": "cpp"
        },
        
        # Java Tests
        {
            "name": "Java - Hello World",
            "code": """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}
""".strip(),
            "language": "java"
        },
        {
            "name": "Java - Array Operations",
            "code": """
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        int sum = Arrays.stream(numbers).sum();
        double average = (double) sum / numbers.length;
        
        System.out.println("Numbers: " + Arrays.toString(numbers));
        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);
    }
}
""".strip(),
            "language": "java"
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
        System.out.println("Words: " + java.util.Arrays.toString(words));
    }
}
""".strip(),
            "language": "java"
        }
    ]
    
    # Track results
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}
    
    for test_case in test_cases:
        success = test_language(
            test_case["name"], 
            test_case["code"], 
            test_case["language"]
        )
        
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        # Small delay between tests
        time.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✅")
    print(f"Failed: {results['failed']} ❌")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    if results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED! The LeetCode Compiler is working perfectly!")
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
