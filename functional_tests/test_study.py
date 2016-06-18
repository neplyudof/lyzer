import unittest
from os import path


class StudyTest(unittest.TestCase):
    def test_extract_file_name_from_file_path_for_mac(self):
        mac_file_path = '/Users/J/Documents/ExampleImage/1.vmem'
        file_name = path.basename(mac_file_path)

        self.assertEqual(file_name, '1.vmem')


if __name__ == '__main__':
    unittest.main()
