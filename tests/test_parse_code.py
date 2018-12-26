import os
import clang
from unittest import TestCase, main
from context import CreateAST


class ParseCode(TestCase):
    def test_create_clang_ast(self):
        test_file_info = {"/tmp/xyz.cpp": ["-I/usr/include"]}

        try:
            CreateAST(test_file_info)
        except clang.cindex.TranslationUnitLoadError as e:
            self.assertTrue("Error parsing translation unit." == str(e))
        except Exception as e:
           self.fail('Unexpected exception raised:', e)
        else:
           self.fail('ExpectedException not raised')

    def test_simple_class_ast(self):
        test_file_name = "/tmp/test.cpp"
        test_file_str  = "class test {int x;};"
        test_file_info = {test_file_name: []}
        with open(test_file_name, "w") as f:
            f.write(test_file_str)

        tu = CreateAST(test_file_info)
        self.assertTrue(test_file_name == tu.spelling)
        children = list(tu.cursor.get_children())
        self.assertTrue(len(children) == 1)

        os.remove(test_file_name)


if __name__ == '__main__':
    main()

