import unittest
from context import ParseSourceCode


class ParseJSON(unittest.TestCase):
    def test_file_exists(self):
        json_file_directory = "/not/exist.json"

        with self.assertAlmostEquals(TypeError):
            parser = ParseSourceCode(json=json_file_directory)


if __name__ == '__main__':
    unittest.main()

