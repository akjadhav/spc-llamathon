class Node:
    def __init__(self, func_name, file_path, line_start, line_end):
        self.func_name = func_name
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end

        self.key = f"{file_path}:{line_start}:{func_name}"