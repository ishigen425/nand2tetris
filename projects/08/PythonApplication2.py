import os, glob
from lib.Parser import Parser
from lib.CodeWriter import CodeWriter


dir = r"./"
# 一つ下のフォルダの.vmファイ5ルを取得
#file_list = glob.glob(dir+"**/*.vm", recursive=True)
#target_dir = "StaticsTest"
#target_dir = "SimpleFunction"
#target_dir = "FibonacciElement"
target_dir = "NestedCall"
file_list = glob.glob(dir+"08/FunctionCalls/" + target_dir + "/*.vm", recursive=True)
output_file_name = os.path.join("08/FunctionCalls/",target_dir,target_dir + ".asm")
# target_file_1 = "08/FunctionCalls/FibonacciElement/Sys.asm"
# target_file_2 = "08/FunctionCalls/FibonacciElement/Main.asm"
#file_name = os.path.basename(file_path)
#output_file_dir = file_path.replace(file_name, "")
#output_file_name = file_name.replace(".vm", ".asm")
code_writer = CodeWriter(output_file_name)
code_writer.write_init()

for file_path in file_list:
    parser = Parser(file_path)
    code_writer.set_file_name(os.path.basename(file_path).replace(".asm", ""))
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "C_ARITHMETIC":
            code_writer.write_artithmetic(parser.arg1())
        elif parser.command_type() == "C_PUSH":
            code_writer.write_push_pop("push", parser.arg1(), parser.arg2())
        elif parser.command_type() == "C_POP":
            code_writer.write_push_pop("pop", parser.arg1(), parser.arg2())
        elif parser.command_type() == "C_LABEL":
            code_writer.write_label(parser.arg1())
        elif parser.command_type() == "C_GOTO":
            code_writer.write_goto(parser.arg1())
        elif parser.command_type() == "C_IF":
            code_writer.write_if(parser.arg1())
        elif parser.command_type() == "C_FUNCTION":
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == "C_RETURN":
            code_writer.write_return()
        elif parser.command_type() == "C_CALL":
            code_writer.write_call(parser.arg1(), parser.arg2())
        
code_writer.close()

# with open(concat_file_name, mode="w") as concat_file:
#     with open(target_file_1) as f:
#         concat_file.write(f.read())
#     with open(target_file_2) as f:
#         concat_file.write(f.read())

