import unittest
from context import ParseSourceCode
from json.decoder import JSONDecodeError


class ParseJSON(unittest.TestCase):
    def test_file_exists(self):
        json_file_directory = "/not/exist.json"

        try:
            parser = ParseSourceCode(json=json_file_directory)
        except FileNotFoundError as e:
            self.assertTrue(True)
        except Exception as e:
           self.fail('Unexpected exception raised:', e)
        else:
           self.fail('ExpectedException not raised')

    def test_file_empty(self):
        empty_file = "/tmp/empty.json"
        with open(empty_file, "w") as f:
            f.write("")

        try:
            parser = ParseSourceCode(json=empty_file)
        except JSONDecodeError as e:
            self.assertTrue(True)
        except Exception as e:
           self.fail('Unexpected exception raised:', e)
        else:
           self.fail('ExpectedException not raised')

    def test_simple_file(self):
        test_file         = "/tmp/test_file.json"
        test_command_file = "FullSystem.cpp"
        test_command_dir  = "/tmp"
        test_command      = "/usr/bin/clang++ %s" % test_command_file

        test_string = '[{"directory": "%s","command": "%s","file": "%s"}]' % (test_command_dir, test_command, test_command_file)

        with open(test_file, "w") as f:
            f.write(test_string)

        commands = ParseSourceCode(json=test_file)

        self.assertEqual(type(commands), dict)
        self.assertEqual(len(commands), 1)
        self.assertIn(test_command_file, commands)
        self.assertEqual(test_command, commands[test_command_file])


if __name__ == '__main__':
    unittest.main()

