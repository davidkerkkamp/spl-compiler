class InputHandler:
    input_text = ""
    lines = []

    @classmethod
    def set_input_text(cls, input_text):
        cls.input_text = input_text
        cls.lines = ''.join(input_text).split('\n')

    @classmethod
    def get_line(cls, number: int):
        length = len(cls.lines)
        if length < 1:
            return ''
        if number <= 1:
            return cls.lines[0]
        if number > length:
            return cls.lines[length - 1]
        return cls.lines[number - 1]


class CodePosition:
    def __init__(self, line, column):
        self.line = line
        self.column = column

    @classmethod
    def from_code_position(cls, position):
        return cls(position.line, position.column)

    def increment_line(self, n=1):
        self.line += n

    def increment_column(self, n=1):
        self.column += n

    def set_column(self, n):
        self.column = n


class CodeRange:
    def __init__(self, start: CodePosition, end: CodePosition):
        self.start = start
        self.end = end

    def __str__(self):
        arrows = ''.join(['^' for x in range(self.end.column - self.start.column)])
        line_and_col_str = '{line}:{col}: '.format(line=self.start.line, col=self.start.column)
        return line_and_col_str + InputHandler.get_line(self.start.line) \
               + '\n' + (''.join([' ' for x in range(len(line_and_col_str) + self.start.column - 1)])) + arrows


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INFO = '\033[34m'
    DEBUG = '\033[32m'
