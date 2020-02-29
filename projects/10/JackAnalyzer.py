# coding:utf-8
from lib import const
from lib.CompilationEngine import CompilationEngine
from lib.JackTokenizer import JackTokenizer
import glob

# folder or file_path
args = r"/home/ishigen/Documents/basic/nand2tetris/projects/10/Square"
file_list = glob.glob(args+"/*.jack")

# first stage
def first_stage_function(file_list):
    for file_path in file_list:
        jack_tokenizer = JackTokenizer(file_path)
        output_file_path = file_path.replace(".jack", "T.xml")
        print(output_file_path)
        with open(output_file_path, mode="w") as output_file:
            output_file.write("<tokens>\n")
            while jack_tokenizer.has_more_tokens():
                jack_tokenizer.advance()
                token_type = jack_tokenizer.token_type()
                if const.KEYWORD == token_type:
                    output_file.write(const.INLINE_TAG_FORMAT.format("keyword", jack_tokenizer.key_word(), "keyword"))
                elif const.SYMBOL == token_type:
                    output_file.write(const.INLINE_TAG_FORMAT.format("symbol", jack_tokenizer.symbol(), "symbol"))
                elif const.IDENTIFIER == token_type:
                    output_file.write(const.INLINE_TAG_FORMAT.format("identifier", jack_tokenizer.identifier(), "identifier"))
                elif const.INT_CONST == token_type:
                    output_file.write(const.INLINE_TAG_FORMAT.format("integerConstant", jack_tokenizer.int_val(), "integerConstant"))
                elif const.STRING_CONST == token_type:
                    output_file.write(const.INLINE_TAG_FORMAT.format("stringConstant", jack_tokenizer.string_val(), "stringConstant"))
                output_file.write("\n")
            output_file.write("</tokens>\n")

#first_stage_function(file_list)

def second_stage_function(file_list):
    for file_path in file_list:
        jack_tokenizer = JackTokenizer(file_path)
        output_file_path = file_path.replace(".jack", ".xml")
        print(output_file_path)
        compile_engine = CompilationEngine(jack_tokenizer, output_file_path)
        compile_engine.create_file()

second_stage_function(file_list)


