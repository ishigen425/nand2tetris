class Parser(object):
    """description of class"""

    def __init__(self, file_path):
        self.C_ARITHMETIC = "C_ARITHMETIC"
        self.C_PUSH = "C_PUSH"
        self.C_POP = "C_POP"
        self.C_LABEL = "C_LABEL"
        self.C_GOTO = "C_GOTO"
        self.C_IF = "C_IF"
        self.C_FUNCTION = "C_FUNCTION"
        self.C_RETURN = "C_RETURN"
        self.C_CALL = "C_CALL"
        with open(file_path) as f:
            asm = f.read()
        self.source_code = []
        for line in asm.split("\n"):
            if not self._is_comment_or_notline(line):
                self.source_code.append(line.split("//")[0].strip())
        self.idx = -1

    def _is_comment_or_notline(self, command):
        if command.strip().startswith("//"):
            return True
        elif len(command.strip()) == 0:
            return True
        return False


    def has_more_commands(self):
        return self.idx + 1 < len(self.source_code)

    def advance(self):
        self.idx += 1
        self.command = self.source_code[self.idx].split()

    def command_type(self):
        if self.command[0] in ("add","sub","neg","eq","gt","lt","and","or","not"):
            return self.C_ARITHMETIC
        if self.command[0] in ("push"):
            return self.C_PUSH
        if self.command[0] in ("pop"):
            return self.C_POP
        if self.command[0] in ("label"):
            return self.C_LABEL
        if self.command[0] in ("goto"):
            return self.C_GOTO
        if self.command[0] in ("if-goto"):
            return self.C_IF
        if self.command[0] in ("function"):
            return self.C_FUNCTION
        if self.command[0] in ("return"):
            return self.C_RETURN
        if self.command[0] in ("call"):
            return self.C_CALL

    def arg1(self):
        assert self.command_type() != self.C_RETURN, "たいぷちがい"
        if self.command_type() == self.C_ARITHMETIC:
            return self.command[0]
        return self.command[1]

    def arg2(self):
        assert self.command_type() in (self.C_PUSH, self.C_POP, self.C_FUNCTION, self.C_CALL), "たいぷちがい"
        return self.command[2]





