import unittest
from ast_parser import AstParser


class AstTest(unittest.TestCase):
    """
    Test AST Parser class
    """

    def test1(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "test1")
        result_attempt = {0: ['x', 'int x=5'], 1: ['y', 'int y=4'], 2: ['x', 'x=5+y']}
        self.assertEqual(ast.variables_dic, result_attempt)

    def test2(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "test2")
        result_attempt = {0: ['y', 'int y=0'], 1: ['z', 'int z=-2'], 2: ['h', 'int h=-5'], 3: ['h', 'h=x-z']}
        self.assertEqual(ast.variables_dic, result_attempt)

    def test3(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "test3")
        #You don't manage pointer
        result_attempt = {0: ['x', 'int x=2']}
        self.assertEqual(ast.variables_dic, result_attempt)

    def test4(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "test4")
        result_attempt = {0: ['x', 'int x=2'], 1: ['h', 'int h=2'], 2: ['x', 'x=z+2']}
        self.assertEqual(ast.variables_dic, result_attempt)

    def test5(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "test5")
        result_attempt = {}
        self.assertEqual(ast.variables_dic, result_attempt)

    def test6(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "test6")
        result_attempt = {0: ['x', 'int x=0']}
        self.assertEqual(ast.variables_dic, result_attempt)

    def testmain(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "main")
        result_attempt = {}
        self.assertEqual(ast.variables_dic, result_attempt)

    def teststruct(self):
        ast = AstParser()
        ast.parse_c_file('input.c', "Client")
        result_attempt = {}
        self.assertEqual(ast.variables_dic, result_attempt)


if __name__ == '__main__':
    unittest.main()



