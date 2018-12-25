import unittest
from context import ParseSourceCode


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

if __name__ == '__main__':
    unittest.main()

