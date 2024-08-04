import re

# def retrieve_output_text(file_path):
#     with open(file_path, 'r') as file:
#         sample_text = file.read()
    
#     return sample_text

def retrieve_jest_test_file(jest_path):
    # Reading the file and storing its contents in a variable.
    with open(jest_path, 'r') as file:
        jest_text = file.read()
    print(jest_text)
    jest_lines = jest_text.split('\n')
    return jest_lines


def map_suites_to_statuses(block):
    global latest_suite
    lines = block.split('\n')
    latest_suite = None
    res = {}

    for line in lines:
        # detect if new suit
        if not line.startswith('   '):
            suit_name = line.strip()
            res[suit_name] = {}
            latest_suite = suit_name
            continue
        
        status = line[4]
        description = line[6:]

        # Regular expression to match and remove the " (...)" part at the end
        pattern = re.compile(r' \(.+\)$')

        # Remove the " (...)" part if present
        description = pattern.sub('', description)

        res[latest_suite][description] = False if status == '✕' else True

    return res

def extract_failed_tests(failed_res, jest_lines):
    failed_context = ""
    failed_details = [] # (line_start, line_finish)

    for suite_name in failed_res:
        print("Suite:" + suite_name)
        describe_pattern = r"describe\(['\"]"

        i = 0
        while i < len(jest_lines):
            match = re.search(describe_pattern + re.escape(suite_name), jest_lines[i])
            i+=1
            if match:
                break

        if i == len(jest_lines):
            print("Suite not found")
            continue
        
        for desc, _ in failed_res[suite_name].items():
            start_index = None
            end_index = None

            for j in range(i, len(jest_lines)):
                it_match = re.search(r"it\(['\"]" + re.escape(desc), jest_lines[j])
                if it_match:
                    start_index = j

            if start_index == None: continue

            for j in range(start_index, len(jest_lines)):
                failed_context += jest_lines[j] + '\n'
                # print(jest_lines[j])
                if jest_lines[j].startswith('  });'):
                    end_index = j
                    break
                    
            end_index = end_index if end_index != None else len(jest_lines)-1
            failed_details.extend(range(start_index, end_index+1))

    return failed_context, failed_details

# def run(file_path, jest_path):
def extract_data(test_out, jest_path):
    # sample_text = retrieve_output_text(file_path)
    jest_lines = retrieve_jest_test_file(jest_path)

    print(test_out)

    # Regular expression to recognize the start of a block and the end of the block
    block_pattern = re.compile(r'(  .+?)(?:\n\s*\n)', re.DOTALL)

    # Finding the first block in the sample text
    match = block_pattern.search(test_out)
    block = match.group(1)
    test_status_mapping = map_suites_to_statuses(block)

    failed_res = {k: {sub_k: sub_v for sub_k, sub_v in v.items() if not sub_v} for k, v in test_status_mapping.items()}
    failed_res = {k: v for k, v in failed_res.items() if v} # remove {} from values

    failed_context, failed_lines = extract_failed_tests(failed_res, jest_lines)

    return test_status_mapping, failed_context, failed_lines


if __name__ == '__main__':
    test_out = """
FAIL utils/math.test.js
  ● Test suite failed to run

    Jest encountered an unexpected token

    Jest failed to parse a file. This happens e.g. when your code or its dependencies use non-standard JavaScript syntax, or when Jest is not configured to support such syntax.

    Out of the box Jest supports Babel, which will be used to transform your files into valid JS based on your Babel configuration.

    By default "node_modules" folder is ignored by transformers.

    Here's what you can do:
     • If you are trying to use ECMAScript Modules, see https://jestjs.io/docs/ecmascript-modules for how to enable it.
     • If you are trying to use TypeScript, see https://jestjs.io/docs/getting-started#using-typescript
     • To have some of your "node_modules" files transformed, you can specify a custom "transformIgnorePatterns" in your config.
     • If you need a custom transformation specify a "transform" option in your config.
     • If you simply want to mock your non-JS modules (e.g. binary assets) you can stub them out with the "moduleNameMapper" config option.

    You'll find more details and examples of these config options in the docs:
    https://jestjs.io/docs/configuration
    For information about custom transformations, see:
    https://jestjs.io/docs/code-transformation

    Details:

    /private/tmp/akjadhav/spc-llamathon-example/utils/math.test.js:144
    import { sumOfSquares } from './math.js';
    ^^^^^^

    SyntaxError: Cannot use import statement outside a module

      at Runtime.createScriptFromCode (../../../../opt/homebrew/lib/node_modules/jest/node_modules/jest-runtime/build/index.js:1505:14)

Test Suites: 1 failed, 1 total
Tests:       0 total
Snapshots:   0 total
Time:        0.129 s
Ran all test suites matching /\/tmp\/akjadhav\/spc-llamathon-example\/utils\/math.test.js/i.
    """
    jest_path = 'sample_data/example.test.js'
    res, failed_context, failed_details = extract_data(test_out, jest_path)

    print(res)
    print(failed_context)
    print(failed_details)