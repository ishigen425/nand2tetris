# coding:utf-8
from lib import const
from lib.JackTokenizer import JackTokenizer
from lib.SymbolTable import SymbolTable
from lib.VMWriter import VMWriter

class CompilationEngine():

    def __init__(self, jack_tokenizer, output_file_path):
        self.is_compiled_class = False
        #self.output_file = open(output_file_path, mode="w")
        self.jack_tokenizer = jack_tokenizer
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file_path)
        self.n_expression_list = 0
        
        
    def create_file(self):
        self.compile_class()
        self._close()

    def _close(self):
        #self.output_file.close()
        self.vm_writer.close()

    def compile_class(self):
        self.is_compiled_class = True
        self.jack_tokenizer.advance()
        self.jack_tokenizer.advance()
        self.class_name = self.jack_tokenizer.identifier()
        self.jack_tokenizer.advance()
        symbol = self.jack_tokenizer.symbol()
        self.field_num = 0
        while self.jack_tokenizer.has_more_tokens():
            self.while_exp_counter = 0
            self.while_end_counter = 0
            self.true_false_counter = 0
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if const.KEYWORD == token_type:
                key_word = self.jack_tokenizer.key_word()
                if key_word in (const.METHOD, const.FUNCTION, const.CONSTRUCTOR):
                    self.symbol_table.start_subroutine()
                    self.compile_subroutine()
                elif key_word in (const.FIELD):
                    self.compile_class_var_dec()
                elif key_word in (const.STATIC):
                    self.compile_class_var_dec()
            else:
                assert True

    def compile_class_var_dec(self):
        assert self.is_compiled_class
        kind = self.jack_tokenizer.key_word()
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == const.KEYWORD:
            _type = self.jack_tokenizer.key_word()
        elif self.jack_tokenizer.token_type() == const.IDENTIFIER:
            _type = self.jack_tokenizer.identifier()
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.IDENTIFIER:
                self.symbol_table.define(self.jack_tokenizer.identifier(), _type, kind)
                if kind == const.FIELD:
                    self.field_num += 1
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";":
                return
    
    def compile_subroutine(self):
        assert self.is_compiled_class
        subroutin_type = self.jack_tokenizer.key_word()
        self.jack_tokenizer.advance()
        self.jack_tokenizer.advance()
        function_name = [self.class_name, ".", self.jack_tokenizer.identifier()]
        self.jack_tokenizer.advance()
        if subroutin_type == "method" and not self.class_name == "Main":
            self.symbol_table.define("this", None, const.ARG)
        # paramterlist
        self.compile_parameter_list()
        # subroutinbody
        self.jack_tokenizer.advance()
        is_start_statements = False
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.KEYWORD and self.jack_tokenizer.key_word() == const.VAR:
                self.compile_var_dec()
                continue
            if not is_start_statements:
                self.vm_writer.write_function("".join(function_name), self.symbol_table.var_count(const.VAR))
                if subroutin_type == "constructor":
                    self.vm_writer.write_push(const.CONSTANT, self.field_num)
                    self.vm_writer.write_call("Memory.alloc", 1)
                    self.vm_writer.write_pop("pointer", 0)
                elif subroutin_type == "method":
                    self.vm_writer.write_push(const.ARGMENT, 0)
                    self.vm_writer.write_pop("pointer", 0)
                is_start_statements = True
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "}":
                break
            self.compile_statements()

    def compile_parameter_list(self):
        assert self.is_compiled_class
        # 一回のループで 型 変数名 のセットを回す
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ")":
                break
            if self.jack_tokenizer.token_type() == const.KEYWORD:
                _type = self.jack_tokenizer.key_word()
            elif self.jack_tokenizer.token_type() == const.IDENTIFIER:
                _type = self.jack_tokenizer.identifier()
            
            self.jack_tokenizer.advance()
            self.symbol_table.define(self.jack_tokenizer.identifier(), _type, const.ARG)
            
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ")":
                break
            


    def compile_var_dec(self):
        assert self.is_compiled_class
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == const.KEYWORD:
            _type = self.jack_tokenizer.key_word()
        elif self.jack_tokenizer.token_type() == const.IDENTIFIER:
            _type = self.jack_tokenizer.identifier()
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.IDENTIFIER:
                self.symbol_table.define(self.jack_tokenizer.identifier(), _type, const.VAR)
            
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";":
                return
        

    def compile_statements(self):
        assert self.is_compiled_class
        # call let, do, if, while, var
        token_type = self.jack_tokenizer.token_type()
        if token_type == const.KEYWORD and self.jack_tokenizer.key_word() == const.LET:
            self.compile_let()
        elif token_type == const.KEYWORD and self.jack_tokenizer.key_word() == const.DO:
            self.compile_do()
        elif token_type == const.KEYWORD and self.jack_tokenizer.key_word() == const.IF:
            self.compile_if()
        elif token_type == const.KEYWORD and self.jack_tokenizer.key_word() == const.WHILE:
            self.compile_while()
        elif token_type == const.KEYWORD and self.jack_tokenizer.key_word() == const.RETURN:
            self.compile_return()


    def compile_do(self):
        assert self.is_compiled_class
        self.jack_tokenizer.advance()
        function_name = []
        option = ""
        self.n_expression_list = 0
        while not (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ("(")):
            function_name.append(self.jack_tokenizer.identifier() if self.jack_tokenizer.token_type() == const.IDENTIFIER else self.jack_tokenizer.symbol())
            self.jack_tokenizer.advance()
        self.jack_tokenizer.advance()
        if len(function_name) == 1:
            function_name = [self.class_name,".",function_name[0]]
            self.vm_writer.write_push("pointer", 0)
            self.n_expression_list += 1
        elif self.symbol_table.kind_of(function_name[0]) == const.FIELD:
            self.vm_writer.write_push(const.THIS, self.symbol_table.index_of(function_name[0]))
            function_name[0] = self.symbol_table.type_of(function_name[0])
            self.n_expression_list += 1
        elif self.symbol_table.kind_of(function_name[0]) == const.VAR:
            function_name[0] = self.symbol_table.type_of(function_name[0])
            self.vm_writer.write_push(const.LOCAL, 0)
            self.n_expression_list += 1
        self.compile_expression_list()
        self.vm_writer.write_call("".join(function_name), self.n_expression_list)
        self.vm_writer.write_pop(const.TEMP, 0)
        self.n_expression_list = 0
        

    def compile_let(self):
        assert self.is_compiled_class
        self._write_to_semicolon()

    def compile_while(self):
        assert self.is_compiled_class
        self.jack_tokenizer.advance()
        self.jack_tokenizer.advance()
        exp_label = "WHILE_EXP{}".format(self.while_exp_counter)
        self.vm_writer.write_label(exp_label)
        self.while_exp_counter += 1
        self.compile_expression()
        self.vm_writer._write_line("not")
        end_label = "WHILE_END{}".format(self.while_end_counter)
        self.while_end_counter += 1
        self.vm_writer.write_if(end_label)
        self.jack_tokenizer.advance()
        self._write_statements()
        self.vm_writer.write_goto(exp_label)
        self.vm_writer.write_label(end_label)
        

    def compile_return(self):
        assert self.is_compiled_class
        self.jack_tokenizer.advance()
        if not (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";"):
            self.compile_expression()
        else:
            self.vm_writer.write_push(const.CONSTANT, "0")
        self.vm_writer.write_return()
        

    def compile_if(self):
        assert self.is_compiled_class
        self.jack_tokenizer.advance()
        self.jack_tokenizer.advance()
        self.compile_expression()
        true_label = "IF_TRUE{}".format(self.true_false_counter)
        false_label = "IF_FALSE{}".format(self.true_false_counter)
        end_label = "IF_END{}".format(self.true_false_counter)
        self.true_false_counter += 1
        self.vm_writer.write_if(true_label)
        self.vm_writer.write_goto(false_label)
        self.vm_writer.write_label(true_label)
        self.jack_tokenizer.advance()
        self._write_statements()
        # 次のトークンを見てelseかどうか判定する
        if self.jack_tokenizer.get_next_token() == const.ELSE:
            self.vm_writer.write_goto(end_label)
            self.vm_writer.write_label(false_label)
            self.jack_tokenizer.advance()
            self.jack_tokenizer.advance()
            self._write_statements()
            self.vm_writer.write_label(end_label)
        else:
            self.vm_writer.write_label(false_label)

        
        

    def compile_expression(self):
        ''' "=" から ";" が出てくるまで 
            "(" から ")" が出てくるまで 
            "[" から "]" が出てくるまで
            expressionタグには0回以上のtermタグが入る
            "=","(" はすでにコンパイルされた状態で使う
            ";", ")", "]" はコンパイルしない
            "=" または "(" の次のtokenの状態で呼び出す
        '''
        assert self.is_compiled_class
        is_first = True
        option = ""
        while True:
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in (")", ";", "]",","):
                break
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ("-") and is_first:
                option = "neg"
                self.compile_term()
            elif self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ("+","*","/","&amp;","|","&lt;","&gt;","=","-","~"):
                option = self.jack_tokenizer.symbol()
            else:
                self.compile_term()
            self.jack_tokenizer.advance()
            is_first = False
        self._compile_option(option)
        

    def compile_term(self):
        assert self.is_compiled_class
        function_name = []
        while True:
            if self.jack_tokenizer.get_next_token() in ("["):
                var_name = self.jack_tokenizer.identifier()
                self.jack_tokenizer.advance()
                self.jack_tokenizer.advance()
                self.compile_expression()
                if self.symbol_table.kind_of(var_name) == const.VAR:
                    self.vm_writer.write_push(const.LOCAL, self.symbol_table.index_of(var_name))
                    is_var = True
                elif self.symbol_table.kind_of(var_name) == const.ARG:
                    self.vm_writer.write_push(const.ARGMENT, self.symbol_table.index_of(var_name))
                    is_var = True
                elif self.symbol_table.kind_of(var_name) == const.FIELD:
                    self.vm_writer.write_push(const.THIS, self.symbol_table.index_of(var_name))
                    is_var = True
                elif self.symbol_table.kind_of(var_name) == const.STATIC:
                    self.vm_writer.write_push(const.STATIC, self.symbol_table.index_of(var_name))
                    is_var = True
                self.vm_writer._write_line("add")
                self.vm_writer.write_pop("pointer", 1)
                self.vm_writer.write_push(const.THAT, 0)
            is_var = False
            if self.jack_tokenizer.token_type() == const.INT_CONST:
                self.vm_writer.write_push(const.CONSTANT, self.jack_tokenizer.int_val())
            elif self.jack_tokenizer.token_type() == const.STRING_CONST:
                self._compile_new_string()
                pass
            elif self.jack_tokenizer.token_type() == const.IDENTIFIER or (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "."):
                # クラス.関数名 or 変数名
                if self.symbol_table.kind_of(self.jack_tokenizer.identifier()) == const.VAR:
                    self.vm_writer.write_push(const.LOCAL, self.symbol_table.index_of(self.jack_tokenizer.identifier()))
                    is_var = True
                elif self.symbol_table.kind_of(self.jack_tokenizer.identifier()) == const.ARG:
                    self.vm_writer.write_push(const.ARGMENT, self.symbol_table.index_of(self.jack_tokenizer.identifier()))
                    is_var = True
                elif self.symbol_table.kind_of(self.jack_tokenizer.identifier()) == const.FIELD:
                    self.vm_writer.write_push(const.THIS, self.symbol_table.index_of(self.jack_tokenizer.identifier()))
                    is_var = True
                elif self.symbol_table.kind_of(self.jack_tokenizer.identifier()) == const.STATIC:
                    self.vm_writer.write_push(const.STATIC, self.symbol_table.index_of(self.jack_tokenizer.identifier()))
                    is_var = True
                if self.jack_tokenizer.get_next_token() == "." or (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "."):
                    function_name.append(self.jack_tokenizer.identifier())
                elif len(function_name) == 2:
                    function_name.append(self.jack_tokenizer.identifier())
            elif self.jack_tokenizer.token_type() == const.KEYWORD:
                if self.jack_tokenizer.key_word() == "true":
                    self.vm_writer.write_push(const.CONSTANT, 0)
                    self.vm_writer._write_line("not")
                elif self.jack_tokenizer.key_word() == "false":
                    self.vm_writer.write_push(const.CONSTANT, 0)
                elif self.jack_tokenizer.key_word() == "this":
                    self.vm_writer.write_push("pointer", 0)
                elif self.jack_tokenizer.key_word() == "null":
                    self.vm_writer.write_push(const.CONSTANT, 0)
            elif self.jack_tokenizer.token_type() == const.SYMBOL:
                if self.jack_tokenizer.symbol() in ("("):
                    self.jack_tokenizer.advance()
                    self.compile_expression()
            else:
                assert False
            # 次のtokenを判定する
            if self.jack_tokenizer.token_type() and const.SYMBOL and self.jack_tokenizer.symbol() in ("~","-"):
                self.jack_tokenizer.advance()
                self.compile_term()

            if self.jack_tokenizer.get_next_token() in ("("):
                self.jack_tokenizer.advance()
                self.jack_tokenizer.advance()
                self.compile_expression_list()
                if len(function_name) == 3:
                    if self.symbol_table.type_of(function_name[0]) != None:
                        self.n_expression_list += 1
                        function_name[0] = self.symbol_table.type_of(function_name[0])
                    self.vm_writer.write_call("".join(function_name), self.n_expression_list)
                    function_name = []
                    self.n_expression_list = 0
            if self.jack_tokenizer.get_next_token() in (".") or (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == (".")):
                self.jack_tokenizer.advance()
                continue
            break
        

    def compile_expression_list(self):
        '''
            "(" が出力されてから呼び出される
            "(" の次のトークンの状態で呼び出す
            ")" は出力しない
        '''
        assert self.is_compiled_class
        #self.n_expression_list = 0
        # 空の場合に対応する
        if not (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ( ")", ";")):
            while True:
                self.n_expression_list += 1
                self.compile_expression()
                if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ( ")", ";"):
                    break
                self.jack_tokenizer.advance()

    def _write_line(self, value):
        self.output_file.write(value + "\n")

    def _write_statements(self):
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "}":
                break
            self.compile_statements()
        
    def _write_to_semicolon(self):
        '''
            semicolonを描画したら処理終了(let 宣言)
        '''
        is_contains_array = False
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.IDENTIFIER:
                var_name = self.jack_tokenizer.identifier()
            
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ("="):
                self.jack_tokenizer.advance()
                self.compile_expression()
                # symbol_tableを見て、イコールの式をここでコンパイルする?
                # 左辺に配列がある場合は、別の処理が必要になる
                if is_contains_array:
                    self.vm_writer.write_pop(const.TEMP, 0)
                    self.vm_writer.write_pop("pointer", 1)
                    self.vm_writer.write_push(const.TEMP, 0)
                    self.vm_writer.write_pop(const.THAT, 0)
                else:
                    if self.symbol_table.kind_of(var_name) == const.VAR:
                        self.vm_writer.write_pop(const.LOCAL, self.symbol_table.index_of(var_name))
                    elif self.symbol_table.kind_of(var_name) == const.ARG:
                        self.vm_writer.write_pop(const.ARGMENT, self.symbol_table.index_of(var_name))
                    elif self.symbol_table.kind_of(var_name) == const.FIELD:
                        self.vm_writer.write_pop(const.THIS, self.symbol_table.index_of(var_name))
                    elif self.symbol_table.kind_of(var_name) == const.STATIC:
                        self.vm_writer.write_pop(const.STATIC, self.symbol_table.index_of(var_name))
            elif self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ("["):
                is_contains_array = True
                self.jack_tokenizer.advance()
                self.compile_expression()
                # symbol_tableを見て、イコールの式をここでコンパイルする?
                if self.symbol_table.kind_of(var_name) == const.VAR:
                    self.vm_writer.write_push(const.LOCAL, self.symbol_table.index_of(var_name))
                elif self.symbol_table.kind_of(var_name) == const.ARG:
                    self.vm_writer.write_push(const.ARGMENT, self.symbol_table.index_of(var_name))
                elif self.symbol_table.kind_of(var_name) == const.FIELD:
                    self.vm_writer.write_push(const.THIS, self.symbol_table.index_of(var_name))
                self.vm_writer._write_line("add")
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ("("):
                self.jack_tokenizer.advance()
                self.compile_expression_list()
                
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";":
                return

    def _compile_option(self, option):
        if option == "+":
            self.vm_writer._write_line("add")
        elif option == "-":
            self.vm_writer._write_line("sub")
        elif option == "*":
            self.vm_writer.write_call("Math.multiply", 2)
        elif option == "/":
            self.vm_writer.write_call("Math.divide", 2)
        elif option == "&gt;":
            self.vm_writer._write_line("gt")
        elif option == "&lt;":
            self.vm_writer._write_line("lt")
        elif option == "~":
            self.vm_writer._write_line("not")
        elif option == "&amp;":
            self.vm_writer._write_line("and")
        elif option == "=":
            self.vm_writer._write_line("eq")
        elif option == "neg":
            self.vm_writer._write_line("neg")
        elif option == "|":
            self.vm_writer._write_line("or")
        elif option == "":
            pass

    def _compile_new_string(self):
        length = len(self.jack_tokenizer.string_val())
        self.vm_writer.write_push(const.CONSTANT, length)
        self.vm_writer.write_call("String.new", 1)
        for i in self.jack_tokenizer.string_val():
            self.vm_writer.write_push(const.CONSTANT, ord(i))
            self.vm_writer.write_call("String.appendChar", 2)

