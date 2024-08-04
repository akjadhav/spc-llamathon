import os
import re
import subprocess
from dotenv import load_dotenv
import pdb
import utils
import json

load_dotenv()

"""
    This class is responsible for generating Jest test cases for JavaScript functions using the BaseTen API.

"""

class Test_Generator:
    def __init__(self, repo_path):
        self.model_id = os.getenv("BASETEN_MODEL_ID")
        self.api_key = os.getenv("BASETEN_API_KEY")
        self.repo_path = repo_path

    def _call_baseten_api(self, prompt):
        messages = [
            {"role": "system", "content": "You are an AI that generates Jest test cases for JavaScript functions."},
            {"role": "user", "content": prompt},
        ]
        
        # output = utils.generate_together(
        #     model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        #     messages=messages,
        #     max_tokens=768,
        #     temperature=0.7,    
        # )

        stream_res = utils.generate_baseten_stream(
            prompt,
            max_tokens=2048,
            temperature=0.7,
        )

        output = ""
        # stream_res will send continuous stream of data
        for content in stream_res:
            output += content.decode("utf-8")
            # TODO: Hook this up this up to the front end so that it will update the output in real time
            # print(output)

        return output
        
    def generate_test(self, target_function_code, target_file_path, context_functions, previous_test_code=None, error_message=None):
        # Construct the prompt
        prompt = (
            "You are an AI that generates Jest test cases for JavaScript functions. I will give you a JavaScript function and its related context functions, and you will generate a Jest test suite for the target function. "
            f"I have the following target JavaScript function code located at this file path: {target_file_path}:\n"
            f"<<FUNCTION target>> {target_function_code} <</FUNCTION target>>\n\n"
            "Here are some context functions that utilize the target function. Do NOT use these functions in the tests. Use these ONLY for context and deciding what tests to write. \n"
        )
        
        for function_info in context_functions:
            function_name, function_code = function_info
            prompt += f"<<FUNCTION {function_name}>> {function_code} <</FUNCTION {function_name}>>\n"
        
        prompt += (
            "Please generate a comprehensive Jest test suite for the target function. You must write ALL test code inside the <<TESTS>> and <</TESTS>> tags.\n"
            "Make sure to include multiple test cases that cover different edge cases and scenarios for the target function.\n"
            "Ensure the output is formatted so that the Jest code is a valid file that can be run directly.\n"
            "Use <<TESTS>> to start and <</TESTS>> to end the test cases section.\n"
            "Ensure that the test suite is valid Jest code that can be run directly.\n"
            "Everything inside the <<TESTS>> and <</TESTS>> tags will be copied directly into a file and run using Jest.\n"
            "Comment your code. \n"
            "You MUST structure your response as follows:\n"
            "<<TESTS>>  // Your Jest code here   <</TESTS>>"
        )

        if previous_test_code and error_message:
            prompt += f"\n\nNote: The previous test suite generated the following error. Please revise the test suite to resolve this error:\n{error_message}"
            prompt += f"\n\nHere is the previous test suite that you generated:\n{previous_test_code}"

        # Call the Baseten API with retries
        test_code = self._call_baseten_api(prompt)
        return test_code

    def _is_test_incorrect(self, test_code, error_message):
        # Construct the prompt to evaluate the test and the error message
        prompt = (
            "You are an AI that evaluates Jest test cases for JavaScript functions. I will give you a Jest test suite and an error message. "
            "Please determine whether the error is due to an issue in the test suite itself or the JavaScript function being tested. "
            "Here is the Jest test suite:\n"
            f"<<TESTS>> {test_code} <</TESTS>>\n\n"
            "Here is the error message:\n"
            f"<<ERROR>> {error_message} <</ERROR>>"
            "Output one of the following:\n"
            "1. The test suite is incorrect and needs to be revised.\n"
            "2. The test suite is correct, and the error is due to an issue in the JavaScript function being tested."
        )

        # Call the Baseten API to evaluate the test and error message
        print("LOG: Evaluating the test suite and error message with LLM")
        evaluation = self._call_baseten_api(prompt)

        # Parse the evaluation to get a boole
        # an
        is_test_incorrect = "The test suite is incorrect" in evaluation
        return is_test_incorrect
            

    def execute_test(self, test_code, file_path=None):
        # Write the test code to a temporary file to check that it works before we add it to the main test file
        directory = os.path.dirname(file_path)
        #_trace()
        test_file_path = os.path.join(directory, "temp.test.js")
        with open(test_file_path, "w") as test_file:
            test_file.write(test_code)
        
        try:
            with open(self.repo_path + '/package.json', 'r') as f:
                package_json = json.load(f)

            if 'jest' not in package_json.get('devDependencies', {}):
                print("Jest not found in devDependencies. Installing...")
                # could use jest --outputFile=<filename> here
                subprocess.run(['npm', 'install', '--save-dev', 'jest'], check=True)

            result = subprocess.run(['npm', 'test', '--', test_file_path], capture_output=True, text=True)
            stdout = result.stdout
            stderr = result.stderr
            # # write stdout and stderr to a file
            # with open("stdout.txt", "w") as file:
            #     file.write(stdout)
            # with open("stderr.txt", "w") as file:
            #     file.write(stderr)
            
            if result.returncode != 0:
                raise Exception(stderr)
        except Exception as e:
            return str(e)
        
        
        main_test_file_path = file_path.replace(".js", ".test.js")
        
        # Test is valid and it works — add it to the main test file!
        # Check if the file exists and set the mode accordingly
        file_mode = 'a' if os.path.exists(main_test_file_path) else 'w'
        
        with open(main_test_file_path, file_mode) as test_file:
            test_file.write(test_code)
        
        return "All tests passed successfully."


    def _extract_tests(self, test_code):
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

    def generate_and_test(self, target_file_info, context_functions):
        error_message = None
        previous_test_code = None
        target_function_code = self.read_functions_from_file(target_file_info[0], target_file_info[1])
        print("LOG: Tests are about to be created for ", target_function_code)
        for attempt in range(5):
            test_code = self.generate_test(target_function_code, target_file_info[0], context_functions, previous_test_code, error_message)
            print("LOG: Tests have been generated by LLM")
            extracted_tests = self._extract_tests(test_code)
            file_path = target_file_info[0]
            print("LOG: Tests have been parsed")

            print(f"LOG: Generated test code:\n{extracted_tests}")
            result = self.execute_test(extracted_tests, file_path)  # Using the target file's path for naming the test file
            if "All tests passed successfully." in result:
                return test_code
            else:
                if self._is_test_incorrect(test_code, result):
                    previous_test_code = test_code
                    # TODO: Handle this so that the new prompt includes the previous fuction code and the error message. 
                    error_message = result
                    print(f"Test is invalid! Attempt {attempt + 1}. Error: {result}")
                else: 
                    print("LOG: Test is correct, but the function is incorrect. ")
                    # The test is correct, but the function is incorrect
                    main_test_file_path = file_path.replace(".js", ".test.js")
        
                    # Test is valid and it works — add it to the main test file!
                    # Check if the file exists and set the mode accordingly
                    file_mode = 'a' if os.path.exists(main_test_file_path) else 'w'
                    
                    with open(main_test_file_path, file_mode) as test_file:
                        test_file.write(extracted_tests)
                    
                    return extracted_tests
        
        raise Exception("Failed to generate a valid test after 5 attempts.")

# Example usage
if __name__ == "__main__":
    test_generator = Test_Generator()
    try:
        target_file_info = ("example.js", ("add", 3, 6))
        context_files_info = [
            ("example.js", "multiply", 8, 11),
            ("example.js", "square", 13, 16),
            ("example.js", "sumOfSquares", 18, 21),
            ("example.js", "factorial", 23, 29),
            ("example.js", "isEven", 31, 34),
            ("example.js", "isOdd", 36, 39),
            ("example.js", "fibonacci", 41, 47)
        ]
        test_code = test_generator.generate_and_test(target_file_info, context_files_info)
        print("Generated test code:\n", test_code)
        
        target_file_info = ("example.js", ("multiply", 8, 11))
        context_files_info = [
            ("example.js", "square", 13, 16),
            ("example.js", "sumOfSquares", 18, 21),
            ("example.js", "factorial", 23, 29),
            ("example.js", "isEven", 31, 34),
            ("example.js", "isOdd", 36, 39),
            ("example.js", "fibonacci", 41, 47)
        ]
        test_code = test_generator.generate_and_test(target_file_info, context_files_info)
        print("Generated test code:\n", test_code)

    except Exception as e:
        print("Failed to generate a passing test:", str(e))
