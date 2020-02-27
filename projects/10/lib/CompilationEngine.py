# coding:utf-8
from lib import const
from JackTokenizer import JackTokenizer

class CompilationEngine():

    def __init__(self, jack_tokenizer, output_file_path):
        self.is_compiled_class = False
        self.output_file = open(output_file_path, mode="w")
        self.jack_tokenizer = jack_tokenizer
        
    def create_file(self):
        self.compile_class()
        self._close()

    def _close(self):
        self.output_file.close()

    def compile_class(self, ):
        self.is_compiled_class = True
        self.jack_tokenizer.advance()
        self._write_line("<class>")
        self._write_line(const.INLINE_KEYWORD_TAG.format("class"))
        self.jack_tokenizer.advance()
        class_name = self.jack_tokenizer.identifier()
        self._write_line(const.INLINE_IDENTIFIER_TAG.format(class_name))
        self.jack_tokenizer.advance()
        symbol = self.jack_tokenizer.symbol()
        self._write_line(const.INLINE_SYMBOL_TAG.format(symbol))
        while self.jack_tokenizer.has_more_tokens():
            self._next()
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        self._write_line("</class>")

    def _next(self):
        if not self.jack_tokenizer.has_more_tokens():
            return
        self.jack_tokenizer.advance()
        token_type = self.jack_tokenizer.token_type()
        if const.KEYWORD == token_type:
            key_word = self.jack_tokenizer.key_word()
            if key_word in (const.METHOD, const.FUNCTION, const.CONSTRUCTOR):
                self.compile_subroutine()
            elif const.VOID == key_word:
                pass
            elif key_word in (const.STATIC, const.FIELD):
                self.compile_class_var_dec()
            elif const.RETURN == key_word:
                self.compile_return()
            else:
                self._write_line(const.INLINE_KEYWORD_TAG.format(key_word))
    
    def compile_class_var_dec(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("classVarDec"))
        self._write_line(const.INLINE_KEYWORD_TAG.format(self.jack_tokenizer.key_word()))
        while True:
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == const.SYMBOL:
                self._write_cmn()
                break
            self._write_cmn()

        self._write_line(const.END_TAG_FORMAT.format("classVarDec"))

    def compile_subroutine(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("subroutineDec"))
        self._write_line(const.INLINE_KEYWORD_TAG.format(self.jack_tokenizer.key_word()))
        for i in range(3):
            self.jack_tokenizer.advance()
            self._write_cmn()

        # paramterlist
        self._write_line(const.START_TAG_FORMAT.format("parameterList"))
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ")":
                break
            self._write_cmn()

        self._write_line(const.END_TAG_FORMAT.format("parameterList"))
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))

        # subroutinbody
        self._write_line(const.START_TAG_FORMAT.format("subroutineBody"))
        self.jack_tokenizer.advance()
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        
        is_start_statements = False
        while self.jack_tokenizer.has_more_tokens():
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.KEYWORD and self.jack_tokenizer.key_word() == const.VAR:
                self.compile_var_dec()
                continue
            if not is_start_statements:
                self._write_line(const.START_TAG_FORMAT.format("statements"))
                is_start_statements = True
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "}":
                break
            self.compile_statements()

        self._write_line(const.END_TAG_FORMAT.format("statements"))
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        self._write_line(const.END_TAG_FORMAT.format("subroutineBody"))
        self._write_line(const.END_TAG_FORMAT.format("subroutineDec"))

    def compile_parameter_list(self):
        assert self.is_compiled_class
        self._next()

    def compile_var_dec(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("varDec"))
        self._write_line(const.INLINE_KEYWORD_TAG.format(self.jack_tokenizer.key_word()))

        while True:
            self.jack_tokenizer.advance()
            token_type = self.jack_tokenizer.token_type()
            if token_type == const.SYMBOL:
                self._write_cmn()
                break
            self._write_cmn()

        self._write_line(const.END_TAG_FORMAT.format("varDec"))

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
        self._write_line(const.START_TAG_FORMAT.format("doStatement"))
        self._write_line(const.INLINE_KEYWORD_TAG.format(self.jack_tokenizer.key_word()))
            
        while True:
            self.jack_tokenizer.advance()
            self._write_cmn()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";":
                break
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "(":
                self.compile_expression_list()
                self._write_cmn()
        
        self._write_line(const.END_TAG_FORMAT.format("doStatement"))

    def compile_let(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("letStatement"))
        self._write_line(const.INLINE_KEYWORD_TAG.format(self.jack_tokenizer.key_word()))

        is_after_symbol = False            
        while True:
            self.jack_tokenizer.advance()
            if is_after_symbol:
                self.compile_expression()
            else:
                self._write_cmn()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";":
                break
            if self.jack_tokenizer.token_type() == const.SYMBOL:
                is_after_symbol = True

        self._write_cmn()
        self._write_line(const.END_TAG_FORMAT.format("letStatement"))

    def compile_while(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("whileStatement"))
        self._write_line(const.INLINE_KEYWORD_TAG.format("while"))
        self.jack_tokenizer.advance()
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
    
        self.jack_tokenizer.advance()
        self.compile_expression()
        self._write_cmn()
        
        self.jack_tokenizer.advance()
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        self._write_line(const.START_TAG_FORMAT.format("statements"))
            
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "}":
                break
            self.compile_statements()

        self._write_line(const.END_TAG_FORMAT.format("statements"))
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        self._write_line(const.END_TAG_FORMAT.format("whileStatement"))

    def compile_return(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("returnStatement"))
        self._write_line(const.INLINE_KEYWORD_TAG.format("return"))
        self.jack_tokenizer.advance()
        if not (self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ";"):
            self.compile_expression()
        
        self._write_cmn()
        self._write_line(const.END_TAG_FORMAT.format("returnStatement"))

    def compile_if(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("ifStatement"))
        self._write_line(const.INLINE_KEYWORD_TAG.format("if"))
        self.jack_tokenizer.advance()
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
    
        self.jack_tokenizer.advance()
        self.compile_expression()
        self._write_cmn()
        
        self.jack_tokenizer.advance()
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        self._write_line(const.START_TAG_FORMAT.format("statements"))
        
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == "}":
                break
            self.compile_statements()

        self._write_line(const.END_TAG_FORMAT.format("statements"))
        self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
        self._write_line(const.END_TAG_FORMAT.format("ifStatement"))

    def compile_expression(self):
        assert self.is_compiled_class
        # = のあとから ; が出てくるまで
        # ( のあとから ) が出てくるまで
        # expressionタグには0回以上のtermタグが入る
        self._write_line(const.START_TAG_FORMAT.format("expression"))
        while True:
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in (")", ";"):
                break
            self.compile_term()
            self.jack_tokenizer.advance()
        self._write_line(const.END_TAG_FORMAT.format("expression"))

    def compile_term(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("term"))
        if self.jack_tokenizer.token_type() == const.INT_CONST:
            self._write_line(const.INLINE_TAG_FORMAT.format("integerConstant",self.jack_tokenizer.int_val(),"integerConstant"))
        elif self.jack_tokenizer.token_type() == const.STRING_CONST:
            self._write_line(const.INLINE_TAG_FORMAT.format("stringConstant",self.jack_tokenizer.string_val(),"stringConstant"))
        elif self.jack_tokenizer.token_type() == const.IDENTIFIER:
            self._write_line(const.INLINE_IDENTIFIER_TAG.format(self.jack_tokenizer.identifier()))
        elif self.jack_tokenizer.token_type() == const.KEYWORD:
            # かっこ以外のsymbolはkeywordタグで出力する
            if self.jack_tokenizer.key_word() in ("(", ")"):
                # "(" を出力して、閉じかっこが出てくるまでexpressionを呼ぶ？
                self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.key_word()))
                # while True:
                #     self.jack_tokenizer.advance()
                #     if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ")":
                #         break
                #     self.jack_tokenizerwhile True:
                #     self.jack_tokenizer.advance()
                #     if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() == ")":
                #         break
                #     self.jack_tokenizer

                # self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.key_word()))

                # self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.key_word()))
            else:
                self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.key_word()))
        self._write_line(const.END_TAG_FORMAT.format("term"))

    def compile_expression_list(self):
        assert self.is_compiled_class
        self._write_line(const.START_TAG_FORMAT.format("expressionList"))
        while True:
            self.jack_tokenizer.advance()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ( ")", ";"):
                break
            self.compile_expression()
            if self.jack_tokenizer.token_type() == const.SYMBOL and self.jack_tokenizer.symbol() in ( ")", ";"):
                break
        self._write_line(const.END_TAG_FORMAT.format("expressionList"))

    def _write_line(self, value):
        self.output_file.write(value + "\n")
    
    def _write_cmn(self):
        token_type = self.jack_tokenizer.token_type()
        if token_type == const.KEYWORD:
            self._write_line(const.INLINE_KEYWORD_TAG.format(self.jack_tokenizer.key_word()))
        elif token_type == const.IDENTIFIER:
            self._write_line(const.INLINE_IDENTIFIER_TAG.format(self.jack_tokenizer.identifier()))
        elif token_type == const.SYMBOL:
            self._write_line(const.INLINE_SYMBOL_TAG.format(self.jack_tokenizer.symbol()))
