from lib import const

class Symbol():

    def __init__(self, _type, kind, idx):
        self._type = _type
        self.kind = kind
        self.idx = idx

    def get_info(self, name):
        if name == "type":
            return self._type
        elif name == "kind":
            return self.kind
        elif name == "idx":
            return self.idx
        else:
            assert False

class SymbolTable():

    def __init__(self):
        self.class_symbol_table = {}
        self.subroutine_symbol_table = {}
        self.class_syombol_idx = 0
        self.subroutine_local_idx = 0
        self.subroutine_arg_idx = 0

    def start_subroutine(self):
        self.subroutine_symbol_table = {}
        self.subroutine_local_idx = 0
        self.subroutine_arg_idx = 0

    def define(self, name, _type, kind):
        if kind in (const.FIELD, const.STATIC):
            symbol = Symbol(_type, kind, self.class_syombol_idx)
            self.class_symbol_table[name] = symbol
            self.class_syombol_idx += 1
        elif kind in (const.VAR):
            symbol = Symbol(_type, kind, self.subroutine_local_idx)
            self.subroutine_symbol_table[name] = symbol
            self.subroutine_local_idx += 1
        elif kind in (const.ARG):
            symbol = Symbol(_type, kind, self.subroutine_arg_idx)
            self.subroutine_symbol_table[name] = symbol
            self.subroutine_arg_idx += 1
        else:
            assert False

    def var_count(self, kind):
        if kind in (const.FIELD, const.STATIC):
            return sum([1 if i.kind == kind else 0 for i in self.class_symbol_table.values()])
        elif kind in (const.VAR, const.ARG):
            return sum([1 if i.kind == kind else 0 for i in self.subroutine_symbol_table.values()])
        else:
            assert False

    def kind_of(self, name):
        if name in self.subroutine_symbol_table.keys():
            return self.subroutine_symbol_table[name].get_info("kind")
        elif name in self.class_symbol_table.keys():
            return self.class_symbol_table[name].get_info("kind")
        else:
            return None

    def type_of(self, name):
        if name in self.subroutine_symbol_table.keys():
            return self.subroutine_symbol_table[name].get_info("type")
        elif name in self.class_symbol_table.keys():
            return self.class_symbol_table[name].get_info("type")
        else:
            return None

    def index_of(self, name):
        if name in self.subroutine_symbol_table.keys():
            return self.subroutine_symbol_table[name].get_info("idx")
        elif name in self.class_symbol_table.keys():
            return self.class_symbol_table[name].get_info("idx")
        else:
            return None
