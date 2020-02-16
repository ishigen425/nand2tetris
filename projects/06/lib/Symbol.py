from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable
import os

def main():
    dir = r"C:\Users\genki_ishikawa\Documents\study\nand2tetris\projects\06\max"
    asm_file = "Max.asm"
    hack_file = asm_file.replace(".asm",".hack")
    input_file = os.path.join(dir, asm_file)
    parser = Parser(input_file)
    output_file = os.path.join(dir, hack_file)
    output = []


    # 疑似コマンド"(Xxxx)"を対象にシンボルテーブルの作成
    symbol = SymbolTable()
    program_counter = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "L_COMMAND":
            symbol.add_entry(parser.symbol()[1:-1], program_counter)
        else:
            program_counter += 1


    code = Code()
    parser = Parser(input_file)
    ramadress_counter = 16
    # ファイルの読み込み
    while parser.has_more_commands():
        parser.advance()
        line = ""
        if parser.command_type() == "L_COMMAND":
            continue
        if parser.command_type() == "A_COMMAND":
            # Aコマンドのときの動作
            # 変数名かどうかの判定
            if parser.symbol()[0].isnumeric():
                # 定数
                address = parser.symbol()
            else:
                # シンボル
                if symbol.contains(parser.symbol()):
                    # 定義済み
                    address = symbol.getAddress(parser.symbol())
                else:
                    # 未定義
                    address = ramadress_counter
                    symbol.add_entry(parser.symbol(), ramadress_counter)
                    ramadress_counter += 1
            line = bin(int(address))[2:]
            line = line.zfill(16)
        elif parser.command_type() == "C_COMMAND":
            # ジャンプのとき
            line = "111"
            line += code.comp(parser.comp())
            line += code.dest(parser.dest())
            line += code.jump(parser.jump())
        output.append(line)

    with open(os.path.join(dir, hack_file), mode='w') as f:
        f.write("\n".join(output))



