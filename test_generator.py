import os
import re
import subprocess
from dotenv import load_dotenv
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
        
    def generate_test(self, target_function_code, target_file_path, context_function_infos, error_message=None):
        # Construct the prompt
        prompt = (
            "I will give you a JavaScript function and its related context functions, and you will generate a Jest test suite for the target function. "
            f"I have the following target JavaScript function code located at this file path: {target_file_path}:\n"
            f"<<FUNCTION target>> {target_function_code} <</FUNCTION target>>\n\n"
            "Here are some context functions related to the target function:\n"
        )
        
        for function_info in context_function_infos:
            function_name, function_code = function_info
            prompt += f"<<FUNCTION {function_name}>> {function_code} <</FUNCTION {function_name}>>\n"
        
        prompt += (
            "Please generate a comprehensive Jest test suite for the target function. You must write ALL test code inside the <<TESTS>> and <</TESTS>> tags.\n"
            "Make sure to include multiple test cases that cover different edge cases and scenarios for the target function.\n"
            "Ensure the output is formatted so that the Jest code is a valid file that can be run directly.\n"
            "Use <<TESTS>> to start and <</TESTS>> to end the test cases section.\n"
            "Ensure that the test suite is valid Jest code that can be run directly.\n"
            "Everything inside the <<TESTS>> and <</TESTS>> tags will be copied directly into a file and run using Jest.\n"
            "Comment your code. Put an error in the code (this is for an exmaple)\n"
            "You MUST structure your response as follows:\n"
            "<<TESTS>>  // Your Jest code here   <</TESTS>>"
        )

        if error_message:
            prompt += f"\n\nNote: The previous test suite generated the following error. Please revise the test suite to resolve this error:\n{error_message}"

        # Call the Baseten API with retries
        test_code = self._call_baseten_api(prompt)
        return test_code

    def execute_test(self, test_code, file_path=None):
        pdb.set_trace()
        test_file_path = file_path.replace(".js", ".test.js")
        with open(test_file_path, 'w') as test_file:
            test_file.write(test_code)

        try:
            result = subprocess.run(['npm', 'test', '--', test_file_path], capture_output=True, text=True)
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
    
    def read_functions_from_file(self, file_path, function_info):
        function_name, start_line, end_line = function_info
        with open(file_path, 'r') as file:
            lines = file.readlines()
            function_code = "".join(lines[start_line-1:end_line])
            
            # Verify the function name is correct
            if not re.search(rf'\bfunction\s+{function_name}\b', function_code):
                raise ValueError(f"Function {function_name} not found in the specified lines.")
            
            return function_code

    def generate_and_test(self, target_file_info, context_files_info):
        error_message = None
        target_function_code = self.read_functions_from_file(target_file_info[0], target_file_info[1])
        context_function_codes = [
            (info[1], self.read_functions_from_file(info[0], info[1:])) for info in context_files_info
        ]
        
        for attempt in range(5):
            test_code = self.generate_test(target_function_code, target_file_info[0], context_function_codes, error_message)
            extracted_tests = self._extract_tests(test_code)

            print(f"Generated test code:\n{test_code}")
            result = self.execute_test(extracted_tests, target_file_info[0])  # Using the target file's path for naming the test file
            if "All tests passed successfully." in result:
                return test_code
            else:
                error_message = result
                print(f"Test failed. Attempt {attempt + 1}. Error: {result}")
        
        raise Exception("Failed to generate a passing test after 5 attempts.")

# Example usage
if __name__ == "__main__":
    test_generator = Test_Generator()
    try:
        target_file_info = ("example.js", ("add", 1, 6))
        context_files_info = [
            ("example.js", "subtract", 8, 13),
            ("example.js", "multiply", 15, 20)
        ]
        test_code = test_generator.generate_and_test(target_file_info, context_files_info)
        print("Generated test code:\n", test_code)
    except Exception as e:
        print("Failed to generate a passing test:", str(e))
