from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable
import os

def main():
    dir = r"C:\Users\genki_ishikawa\Documents\study\nand2tetris\projects\06\rect"
    asm_file = "RectL.asm"
    hack_file = asm_file.replace(".asm",".hack")
    input_file = os.path.join(dir, asm_file)
    parser = Parser(input_file)
    output_file = os.path.join(dir, hack_file)
    output = []

    code = Code()

    # ファイルの読み込み
    while parser.has_more_commands():
        parser.advance()
        line = ""
        if parser.command_type() == "A_COMMAND":
            # Aコマンドのときの動作
            line = bin(int(parser.symbol()))[2:]
            line = line.zfill(16)
        elif parser.command_type() == "C_COMMAND":
            # ジャンプのとき
            line = "111"
            line += code.comp(parser.comp())
            line += code.dest(parser.dest())
            line += code.jump(parser.jump())
        else:
            # その他のCコマンド
            line = "111"
            line += code.comp(parser.comp())
            line += code.dest(parser.dest())
            line += code.jump(parser.jump())
        output.append(line)

    with open(os.path.join(dir, hack_file), mode='w') as f:
        f.write("\n".join(output))



