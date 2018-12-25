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

    def test_parse_two_files(self):
        test_command_file = ["1.cpp", "2.cpp"]
        test_command_dir  = "/tmp"
        test_command      = ["/usr/bin/clang++ %s" % test_command_file[0],
                                "/usr/bin/clang++ %s" % test_command_file[1]]

        test_full_string = """
[
{"directory": "%s","command": "%s","file": "%s"},
{"directory": "%s","command": "%s","file": "%s"}
]
""" % (test_command_dir, test_command[0], test_command_file[0],
       test_command_dir, test_command[1], test_command_file[1])

        test_string = io.StringIO(test_full_string)

        commands = ParseSourceCode(json=test_string)

        self.assertEqual(type(commands), dict)
        self.assertEqual(len(commands), 2)

        keys = list(commands.keys())
        for index, (test_file, true_file) in enumerate(zip(keys, test_command_file)):
            self.assertEqual(test_file, true_file)
            self.assertEqual(commands[test_file], test_command[index])


if __name__ == '__main__':
    main()

