import re

def retrieve_output_text(file_path):
    with open(file_path, 'r') as file:
        sample_text = file.read()
    
    return sample_text

def retrieve_jest_test_file(file_path):
    # Reading the file and storing its contents in a variable.
    with open(jest_path, 'r') as file:
        jest_text = file.read()
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
                    
            failed_details.append((start_index, end_index != None and end_index or len(jest_lines)-1))

    return failed_context, failed_details

def run(file_path, jest_path):
    sample_text = retrieve_output_text(file_path)

    # Regular expression to recognize the start of a block and the end of the block
    block_pattern = re.compile(r'(  .+?)(?:\n\s*\n)', re.DOTALL)

    # Finding the first block in the sample text
    match = block_pattern.search(sample_text)
    block = match.group(1)
    res = map_suites_to_statuses(block)
    # extract failed tests

    failed_res = {k: {sub_k: sub_v for sub_k, sub_v in v.items() if not sub_v} for k, v in res.items()}
    failed_res = {k: v for k, v in failed_res.items() if v} # remove {} from values

    jest_lines = retrieve_jest_test_file(jest_path)
    failed_context, failed_details = extract_failed_tests(failed_res, jest_lines)

    return res, failed_context, failed_details


file_path = 'sample_data/stderr.txt'
jest_path = 'sample_data/example.test.js'
res, failed_context, failed_details = run(file_path, jest_path)
