import io
from unittest import TestCase, main
from context import ParseSourceCode
from json.decoder import JSONDecodeError


class ParseJSON(TestCase):
    def test_file_empty(self):
        try:
            empty_file = io.StringIO("")
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

        test_string = io.StringIO('[{"directory": "%s","command": "%s","file": "%s"}]' % (test_command_dir, test_command, test_command_file))

        commands = ParseSourceCode(json=test_string)

        self.assertEqual(type(commands), dict)
        self.assertEqual(len(commands), 1)
        self.assertIn(test_command_file, commands)
        self.assertEqual(test_command, commands[test_command_file])


if __name__ == '__main__':
    main()

