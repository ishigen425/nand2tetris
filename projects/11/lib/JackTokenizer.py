from lib import const
import re

class JackTokenizer():

    def __init__(self, path):
        print(__file__)
        self.idx = -1
        self.input_file = []
        with open(path) as f:
            lines = f.read()
        is_multi_comment_line = False
        for l in lines.split("\n"):
            if self._is_mult_comment_end(l):
                is_multi_comment_line = False
            elif self._is_mult_comment_start(l):
                is_multi_comment_line = True
            elif is_multi_comment_line:
                continue
            elif self._is_comment_or_notline(l):
                continue
            else:
                l = l.split("//")[0].strip()
                l = self._split(l)
                for symbol in const.ALL_SYMBOL:
                    l = self._parse_symbol(l, symbol)
                self.input_file.extend(l)
        self.command = ""

    def has_more_tokens(self):
        return self.idx + 1 < len(self.input_file)
    
    def _parse_symbol(self, value, symbol):
        ret = []
        for token in value:
            if symbol in token:
                ret.extend(self._split_symbol(token, symbol))
            else:
                ret.append(token)
        return ret

    def _split(self, value):
        is_quote = False
        tmp = ""
        ret = []
        for v in value.strip():
            if v in (" ", "\t") and not is_quote:
                if tmp != "":
                    ret.append(tmp)
                    tmp = ""
            elif v == "\"":
                is_quote = not is_quote
                tmp += v
            else:
                tmp += v
        if tmp != "":
            ret.append(tmp)
        return ret

    def _split_symbol(self, value, symbol):
        tmp = ""
        ret = []
        is_quote = False
        for v in value:
            if v == "\"":
                is_quote = not is_quote
                tmp += v
            elif v in (symbol) and not is_quote:
                if tmp != "":
                    ret.append(tmp)
                    tmp = ""
                ret.append(symbol)
            else:
                tmp += v
        if tmp != "":
            ret.append(tmp)
        return ret

    def _is_comment_or_notline(self, command):
        if command.strip().startswith("//"):
            return True
        elif len(command.strip()) == 0:
            return True
        return False
    
    def _is_mult_comment_start(self, command):
        if "/*" in command:
            return True
        return False

    def _is_mult_comment_end(self, command):
        if "*/" in command:
            return True
        return False

    def advance(self):
        self.idx += 1
        if self.idx < len(self.input_file):
            self.token = self.input_file[self.idx].strip()

    def token_type(self):
        if self.token in ("class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","while","return","let","else","do","if"):
            return const.KEYWORD
        if self.token in const.ALL_SYMBOL:
            return const.SYMBOL
        if re.sub("[^0-9]","",self.token) == self.token and 0 <= int(self.token) <= 32767:
            return const.INT_CONST
        if re.sub("[^a-zA-Z_]","",self.token) == self.token:
            return const.IDENTIFIER
        if re.sub("[\"\n]","",self.token) == self.token[1:-1]:
            return const.STRING_CONST

    def key_word(self):
        return self.token

    def symbol(self):
        return self.token.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

    def identifier(self):
        return self.token
    
    def int_val(self):
        return self.token

    def string_val(self):
        return self.token[1:-1]
    
    def get_next_token(self):
        if self.idx + 1 < len(self.input_file):
            return self.input_file[self.idx+1].strip()
        return self.token
    
