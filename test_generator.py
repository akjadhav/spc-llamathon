import requests
from dotenv import load_dotenv
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import subprocess
import re
import pdb
import utils
load_dotenv()

class Test_Generator:
    def __init__(self):
        self.model_id = os.getenv("BASETEN_MODEL_ID")
        self.api_key = os.getenv("BASETEN_API_KEY")

    def _call_baseten_api(self, prompt):
        messages = [
            {"role": "system", "content": "You are an AI that generates Jest test cases for JavaScript functions."},
            {"role": "user", "content": prompt},
        ]
        
        output = utils.generate_together(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=messages,
            max_tokens=768,
            temperature=0.7,    
        )

        # print("Calling Baseten API with prompt:", prompt)

        # response = requests.post(
        #     f"https://model-{self.model_id}.api.baseten.co/production/predict",
        #     headers={"Authorization": f"Api-Key {self.api_key}"},
        #     json=data
        # )
        
        return output
        
    def generate_test(self, function_code, error_message=None):
        # Construct the prompt
        prompt = (
            f"I will give you a JavaScript function and you will generate a Jest test suite for it. "
            f"I have the following JavaScript function code: <<FUNCTION>> {function_code} <</FUNCTION>>. "
            f"Please generate a comprehensive Jest test suite for this function. Write all test code inside the <<TESTS>> and <</TESTS>> "
            f"Make sure to include multiple test cases that cover different edge cases and scenarios. "
            f"Ensure the output is formatted so that the Jest code is a valid file that can be run directly. "
            f"Use <<TESTS>> to start and <</TESTS>> to end the test cases section. "
            f"Ensure that the test suite is valid Jest code that can be run directly. DO NOT "
            f"Everything inside the <<TESTS>> and <</TESTS>> tags will be copied directly into a file and run using Jest. "
            f"Comment your code. "
            f"Structure your response as follows: "
            f"<<TESTS>>  // Your Jest code here   <</TESTS>>"
)
        if error_message:
            prompt += f"\n\nNote: The previous test suite generated the following error. Please revise the test suite to fix the error:\n{error_message}"

        # Call the Baseten API with retries
        test_code = self._call_baseten_api(prompt)
        return test_code

    def execute_test(self, test_code):
        pdb.set_trace()

        with open('test_generated.js', 'w') as test_file:
            test_file.write(test_code)
        
        try:
            result = subprocess.run(['jest', 'test_generated.js'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(result.stderr)
        except Exception as e:
            return str(e)
        
        return "All tests passed successfully."

    def _extract_tests(self, test_code):
        pdb.set_trace() 
        # Use regex to extract the test cases
        match = re.search(r'<<TESTS>>(.*?)<</TESTS>>', test_code, re.DOTALL)
        if not match:
            raise ValueError("No test cases found in the generated code.")
        
        extracted_tests = match.group(1).strip()
        return extracted_tests

    def generate_and_test(self, function_code):
        error_message = None
        # for _ in range(5):  # Retry up to 5 times
        test_code = self.generate_test(function_code, error_message)
        extracted_tests = self._extract_tests(test_code)

        print(f"Generated test code:\n{test_code}")
        result = self.execute_test(extracted_tests)
        if "All tests passed successfully." in result:
            return test_code
        else:
            error_message = result
        
        raise Exception("Failed to generate a passing test after 5 attempts.")

# Example usage
if __name__ == "__main__":
    function_code = """
    function add(a, b) {
        if (typeof a !== 'number' || typeof b !== 'number') {
            throw new Error('Both arguments must be numbers');
        }
        return a + b;
    }
    """
    
    test_generator = Test_Generator()
    try:
        test_code = test_generator.generate_and_test(function_code)
        print("Generated test code:\n", test_code)
    except Exception as e:
        print("Failed to generate a passing test:", str(e))
