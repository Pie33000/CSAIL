from __future__ import print_function
from pycparser import c_parser, c_ast, parse_file
import sys
sys.path.extend(['.', '..'])
from pycparser import c_parser, c_ast

class AstParser:

    def __init__(self):
        self.variables_dic = {}
        self.values = None
        self.expr = []

    def parse_c_file(self, filename, function_name):
        parser = c_parser.CParser()
        ast = parse_file(filename)
        function_decl = ast.ext
        for i in function_decl:
            if i.decl.name == function_name:
                self.values = i
        variables = self.values.body.block_items
        for i, j in enumerate(variables):
            try:
                self.variables_dic[i] = [j.name, j.init.type+' '+j.name+"="+j.init.value]
            except:
                try:
                    self.expr.append(j.lvalue.name)
                    self.expr.append(j.op)
                    self.parse_tree(j.rvalue, i)
                except:
                    print("This node is not a Binary assignment")


    def parse_tree(self, rvalue, i):
        try:
            try:
                self.expr.append(rvalue.right.value)
                self.expr.append(rvalue.op)
            except:
                self.expr.append(rvalue.right.name)
                self.expr.append(rvalue.op)
            self.parse_tree(rvalue.left, i)
        except:
            try:
                self.expr.append(rvalue.left.name)
                expr = ''.join(self.expr)
                self.variables_dic[i] = [self.expr[0], expr]
                self.expr = []
            except:
                self.expr.append(rvalue.left.value)
                expr = ''.join(self.expr)
                self.variables_dic[i] = [self.expr[0], expr]
                self.expr = []

