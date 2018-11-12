from __future__ import print_function
from pycparser import c_parser, c_ast, parse_file
import sys
import logging
sys.path.extend(['.', '..'])
from pycparser import c_parser, c_ast
from pycparser.plyparser import ParseError
from logging.handlers import RotatingFileHandler


class AstParser:
    """
    Abstract Syntax Tree Parser
        Features :
        -Parse C file, find variable declaration(int, float, double) and binary operation
    """

    def __init__(self):

        self.variables_dic = {}
        self.values = None
        self.expr = []
        self.declarations = "<class 'pycparser.c_ast.Decl'>"
        self.binary_assignment = "<class 'pycparser.c_ast.Assignment'>"
        self.binary_op = "<class 'pycparser.c_ast.BinaryOp'>"
        self.logger = None
        self.log_activity_initializer('activity.log')
        self.id_node = 0
        self.error_bool = False

    def log_activity_initializer(self, filename):
        """
        log_activity_initializer : initilize log file
        :param filename: a .log file
        :return:
        """
        if filename:
            try:
                self.logger = logging.getLogger()
                self.logger.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
                file_handler = RotatingFileHandler(filename, 'a', 1000000, 1)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception:
                self.logger.error('Unknown exception in log_activity_initializer function')
        else:
            self.logger.error('You must pass a filename')

    def parse_c_file(self, filename, function_name):
        """

        :param filename:
        :param function_name: name of a function in a C file, filename
        :return: a dictionary that includes variable declarations and binary operations
        """
        parser = c_parser.CParser()
        #try/catch error due to C code
        try:
            ast = parse_file(filename)
        except:
            self.logger.error('You must verify your C file syntax')
            return
        function_decl = ast.ext
        for i in function_decl:
            try:
                if i.decl.name == function_name:
                    self.values = i
            except:
                pass
        try:
            variables = self.values.body.block_items
            for i, j in enumerate(variables):
                if str(type(j)) == self.declarations:
                    try:
                        op = j.init.op
                        self.variables_dic[self.id_node] = [j.name, j.init.expr.type+' '+j.name+"="+op+j.init.expr.value]
                        self.id_node += 1
                    except:
                        try:
                            self.variables_dic[self.id_node] = [j.name, j.init.type + ' ' + j.name + "=" + j.init.value]
                            self.id_node += 1
                        except:
                            self.logger.error('This type of data is unknow %s', str(type(j)))
                            self.error_bool = True
                elif str(type(j)) == self.binary_assignment:
                    if str(type(j.rvalue)) == self.binary_op:
                        self.expr.append(j.lvalue.name)
                        self.expr.append(j.op)
                        self.parse_tree_bin_op(j.rvalue)
                    else:
                        self.logger.error('This type of data is unknow %s', str(type(j.rvalue)))
                        self.error_bool = True
                else:
                    self.logger.error('This type of data is unknow %s', str(type(j)))
                    self.error_bool = True
        except:
            pass

    def parse_tree_bin_op(self, rvalue):
        """
        parse_tree_bin_op : parse binary operation
        :param rvalue: an object that contains left and right node
        :return:
        """
        try:
            try:
                self.expr.append(rvalue.right.value)
                self.expr.append(rvalue.op)
            except:
                self.expr.append(rvalue.right.name)
                self.expr.append(rvalue.op)
            self.parse_tree_bin_op(rvalue.left)
        except:
            try:
                self.expr.append(rvalue.left.name)
                expr = ''.join(self.expr)
                self.variables_dic[self.id_node] = [self.expr[0], expr]
                self.id_node += 1
                self.expr = []
            except:
                self.expr.append(rvalue.left.value)
                expr = ''.join(self.expr)
                self.variables_dic[self.id_node] = [self.expr[0], expr]
                self.id_node += 1
                self.expr = []
