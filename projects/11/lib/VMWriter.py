from lib import const

class VMWriter():

    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, "w")
    
    def write_push(self, segment, index):
        self._write_line("push {} {}".format(segment, index))

    def write_pop(self, segment, index):
        self._write_line("pop {} {}".format(segment, index))

    def write_artithmetic(self, command):
        pass

    def write_label(self, label):
        self._write_line("label {}".format(label))

    def write_goto(self, label):
        self._write_line("goto {}".format(label))

    def write_if(self, label):
        self._write_line("if-goto {}".format(label))

    def write_call(self, name, n_args):
        self._write_line("call {} {}".format(name, n_args))
        #self.write_pop("temp","0")

    def write_function(self, name, n_locals):
        self._write_line("function {} {}".format(name, n_locals))

    def write_return(self):
        self._write_line("return")

    def close(self):
        self.output_file.close()

    def _write_line(self, value):
        self.output_file.write(value + "\n")
