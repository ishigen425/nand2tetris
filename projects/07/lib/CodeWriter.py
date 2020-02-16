class CodeWriter(object):
    """description of class"""

    def __init__(self, file_path):
        self._stack_pointer_countup = "@SP\nM=M+1\n"
        self._stack_pointer_countdown = "@SP\nM=M-1\n"
        self._stack_push_d_reg = "@SP\nA=M\nM=D\n"
        self.write_file = open(file_path, mode="w")
        self.jump_counter = 0

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_artithmetic(self, command):
        if command == "add":
            self.write_file.write(self._stack_pointer_countdown + "A=M\nD=M\n" + self._stack_pointer_countdown + "A=M\nM=M+D\n" + self._stack_pointer_countup)
        elif command == "sub":
            self.write_file.write(self._stack_pointer_countdown + "A=M\nD=M\n" + self._stack_pointer_countdown + "A=M\nM=M-D\n" + self._stack_pointer_countup)
        elif command == "neg":
            self.write_file.write(self._stack_pointer_countdown + "A=M\nM=-M\n" + self._stack_pointer_countup)
        elif command == "and":
            self.write_file.write(self._stack_pointer_countdown + "A=M\nD=M\n" + self._stack_pointer_countdown + "A=M\nM=M&D\n" + self._stack_pointer_countup)
        elif command == "or":
            self.write_file.write(self._stack_pointer_countdown + "A=M\nD=M\n" + self._stack_pointer_countdown + "A=M\nM=M|D\n" + self._stack_pointer_countup)
        elif command == "not":
            self.write_file.write(self._stack_pointer_countdown + "A=M\nM=!M\n" + self._stack_pointer_countup)
        else:
            # ジャンプが必要なコマンドは別関数で定義
            self.write_file.write(self._make_jump_command(command))

    def write_push_pop(self, command, segment, index):
        # pushのときとpopのときで動作を変える
        if command == "push":
            if segment== "constant":
                self.write_file.write("@{}\nD=A\n@SP\nA=M\nM=D\n".format(index) + self._stack_pointer_countup)
            elif segment == "local":
                self.write_file.write(self._make_push_command("LCL", index))
            elif segment == "argument":
                self.write_file.write(self._make_push_command("ARG", index))
            elif segment == "this":
                self.write_file.write(self._make_push_command("THIS", index))
            elif segment == "that":
                self.write_file.write(self._make_push_command("THAT", index))
            elif segment == "temp":
                self.write_file.write(self._make_push_command("R{}".format(int(index)+5), index, False))
            elif segment == "pointer":
                if index == "0":
                    self.write_file.write(self._make_push_command("THIS", index, False))
                    self.write_file.write("@THIS\nD=M\n")
                elif index == "1":
                    self.write_file.write(self._make_push_command("THAT", index, False))
            elif segment == "static":
                self.write_file.write(self._make_push_command("{}.{}".format(self.file_name, index), index, False))
        elif command == "pop":
            if segment == "local":
                self.write_file.write(self._make_pop_command("LCL", index))
            elif segment == "argument":
                self.write_file.write(self._make_pop_command("ARG", index))
            elif segment == "this":
                self.write_file.write(self._make_pop_command("THIS", index))
            elif segment == "that":
                self.write_file.write(self._make_pop_command("THAT", index))
            elif segment == "temp":
                self.write_file.write(self._make_pop_command("R{}".format(int(index)+5), index, False))
            elif segment == "pointer":
                if index == "0":
                    self.write_file.write(self._make_pop_command("THIS", index, False))
                elif index == "1":
                    self.write_file.write(self._make_pop_command("THAT", index, False))
            elif segment == "static":
                self.write_file.write(self._make_pop_command("{}.{}".format(self.file_name, index), index, False))

    def _make_push_command(self, segment, index, is_calc_index=True):
        if is_calc_index:
            return "@{}\nD=M\n@{}\nA=D+A\nD=M\n".format(segment, index) + self._stack_push_d_reg + self._stack_pointer_countup
        else:
            return "@{}\nD=M\n".format(segment) + self._stack_push_d_reg + self._stack_pointer_countup



    def _make_pop_command(self, segment, index, is_calc_index=True):
        if is_calc_index:
            return self._make_add_segment(segment, index) + self._stack_pointer_countdown + "A=M\nD=M\n" + "@{}\nA=M\nM=D\n".format(segment) + self._make_sub_segment(segment, index)
        else:
            return self._stack_pointer_countdown + "A=M\nD=M\n" + "@{}\nM=D\n".format(segment)


    def _make_add_segment(self, segment, index):
        return "@{}\nD=A\n@{}\nM=M+D\n".format(index, segment)

    def _make_sub_segment(self, segment, index):
        return "@{}\nD=A\n@{}\nM=M-D\n".format(index, segment)

    def close(self):
        self.write_file.write("(END)\n@END\n0;JMP\n")
        self.write_file.close()

    def _make_jump_command(self, command):
        # x-yをじっし
        ret = self._stack_pointer_countdown + "A=M\nD=M\n" + self._stack_pointer_countdown + "A=M\nD=M-D\n"
        ret += "@TRUE{}\n".format(self.jump_counter)
        # commandに応じて、現在のメモリ値を参照して処理を実施
        if command == "eq":
            ret += "D;JEQ\n"
        elif command == "gt":
            ret += "D;JGT\n"
        elif command == "lt":
            ret += "D;JLT\n"
        ret += "@FALSE{}\n0;JMP\n".format(self.jump_counter)
        # ジャンプ先の定義
        ret += "(TRUE{})\n@1\nD=A\n@SP\nA=M\nM=D\nM=-M\n@NEXT{}\n0;JMP\n(FALSE{})\n@0\nD=A\n@SP\nA=M\nM=D\n".format(self.jump_counter, self.jump_counter, self.jump_counter)
        ret += "(NEXT{})\n".format(self.jump_counter)
        self.jump_counter += 1
        return ret + self._stack_pointer_countup

