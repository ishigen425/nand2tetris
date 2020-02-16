import os, glob
from lib.Parser import Parser
from lib.CodeWriter import CodeWriter


dir = r"C:\Users\genki_ishikawa\Documents\study\nand2tetris\projects\07\\"
# 一つ下のフォルダの.vmファイ5ルを取得
file_list = glob.glob(dir+"**/*.vm", recursive=True)

for file_path in file_list:
    parser = Parser(file_path)
    file_name = os.path.basename(file_path)
    output_file_dir = file_path.replace(file_name, "")
    output_file_name = file_name.replace(".vm", ".asm")
    code_writer = CodeWriter(os.path.join(output_file_dir, output_file_name))
    code_writer.set_file_name(output_file_name.replace(".asm", ""))
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "C_ARITHMETIC":
            code_writer.write_artithmetic(parser.arg1())
        elif parser.command_type() == "C_PUSH":
            code_writer.write_push_pop("push", parser.arg1(), parser.arg2())
        elif parser.command_type() == "C_POP":
            code_writer.write_push_pop("pop", parser.arg1(), parser.arg2())

    code_writer.close()

