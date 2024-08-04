class GraphNode:
    def __init__(self, func_name, file_path, line_start, line_end, changed=False):
        self.func_name = func_name
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end

        self.changed = changed

        # self.key = f"{file_path}:{line_start}:{func_name}"
        # self.key = f"{file_path}:{func_name}"
        self.rebuild_key()

    def rebuild_key(self):
        self.key = f"{self.file_path}:{self.func_name}"

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.key == other.key
        return False

    def __hash__(self):
        return hash(self.key)

    def toString(self):
        return f"In {self.file_path}, function {self.func_name} from lines {self.line_start}:{self.line_end} changed."
    
    def __str__(self):
        return self.key
    
    def get_code(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            code_lines = lines[self.line_start-1:self.line_end]
            code = ''.join(code_lines)
            return (self.file_path, self.func_name, code)