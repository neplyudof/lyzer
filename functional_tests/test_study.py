import unittest
from os import path

from memsis.volinterface import RunVol


class StudyTest(unittest.TestCase):
    def test_extract_file_name_from_file_path_for_mac(self):
        file_path = '/home/parallels/Documents/ExampleImage/1.vmem'
        file_name = path.basename(file_path)
        vol = RunVol(mem_path=file_path)
        json = vol.run_plugin('imageinfo')
        print json

        self.assertEqual(file_name, '1.vmem')


if __name__ == '__main__':
    unittest.main()
