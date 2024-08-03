class GraphNode:
    def __init__(self, func_name, file_path, line_start, line_end):
        self.func_name = func_name
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end

        self.key = f"{file_path}:{line_start}:{func_name}"

    def toString(self):
        return f"In {self.file_path}, function {self.func_name} from lines {self.line_start}:{self.line_end} changed."