from unittest import TestCase, main
from context import CreateAST

class ParseCode(TestCase):
    def test_create_clang_ast(self):
        test_file_info = {"/tmp/test.cpp": ["-I/usr/include"]}

        CreateAST(test_file_info)

if __name__ == '__main__':
    main()

