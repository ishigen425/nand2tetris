# coding:utf-8
from lib import const
from lib.CompilationEngine import CompilationEngine
from lib.JackTokenizer import JackTokenizer
import glob, os

# folder or file_path
args = r"/home/ishigen/Documents/basic/nand2tetris/projects/11/ConvertToBin/"
if os.path.isfile(args):
    file_list = [args]
else:
    file_list = glob.glob(args+"/*.jack")

def second_stage_function(file_list):
    for file_path in file_list:
        jack_tokenizer = JackTokenizer(file_path)
        output_file_path = file_path.replace(".jack", ".vm")
        print(output_file_path)
        compile_engine = CompilationEngine(jack_tokenizer, output_file_path)
        compile_engine.create_file()

second_stage_function(file_list)


