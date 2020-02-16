class Parser(object):
    """description of class"""
    # 構文解析を行うクラス


    def __init__(self, file_path):
        self.A = "A_COMMAND"
        self.C = "C_COMMAND"
        self.L = "L_COMMAND"
        self.DEST_LIST = ("JGT","JEQ","JGE","JLT","JNE","JLE","JMP")
        with open(file_path) as f:
            asm = f.read()
        self.assembler = []
        for line in asm.split("\n"):
            if not self._is_comment_or_notline(line):
                self.assembler.append(line.split("//")[0].strip())
        self.idx = -1
        self.command = ""

    def has_more_commands(self):
        return self.idx + 1 < len(self.assembler)

    def _is_comment_or_notline(self, command):
        if command.strip().startswith("//"):
            return True
        elif len(command.strip()) == 0:
            return True
        return False

    def advance(self):
        self.idx += 1
        if self.idx < len(self.assembler):
            self.command = self.assembler[self.idx].strip()

    def _is_jump(self, command):
        for l in self.DEST_LIST:
            if l in command:
                return True
        return False

    def command_type(self):
        if self.command[0] == "@":
            return self.A
        elif self.command.startswith("("):
            return self.L
        else:
            return self.C
        
    def symbol(self):
        if self.command_type() == self.C:
            pass
        return self.command.lstrip("@")

    def dest(self):
        if "=" in self.command:
            return self.command.split("=")[0]
        return ""

    def comp(self):
        # 0;JMPのときにうまく返せていないはず
        if ";" in self.command:
            return self.command.split(";")[0]
        if "=" in self.command:
            return self.command.split("=")[1]
        return self.command[2:]

    def jump(self):
        if ";" in self.command:
            return self.command[-3:]
        return ""
    
