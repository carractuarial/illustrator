from tempfile import TemporaryDirectory
import unittest

from illustrator import data_functions

class Test_Data_Functions(unittest.TestCase):

    def test_read_flat_csv(self):
        # add a temporary directory
        temp_dir = self.enterContext(TemporaryDirectory(dir='.'))

        # create a temporary file and write dummy data to it
        temp_file_name = temp_dir + '/temp.csv'
        with open(temp_file_name, mode='w+') as temp_file:
            temp_file.writelines(['Rate\n','0.123'])
        
        # confirm the _read_flat_csv function returns a list of length 120 with desired data
        self.assertEqual(data_functions.read_flat_csv(temp_file_name), [0.123]*120)

    def test_read_flat_csv_incorrect_data_fail(self):
        temp_dir = self.enterContext(TemporaryDirectory(dir='.'))
        temp_file_name = temp_dir + '/temp.csv'
        with open(temp_file_name, mode='w+') as temp_file:
            temp_file.writelines(['Rate\n','0.123'])
        self.assertNotEqual(data_functions.read_flat_csv(temp_file_name), [0.0]*120)

    def test_get_policy_fee(self):
        self.assertEqual(data_functions.read_flat_csv('./data/policy_fee.csv'),[120]*120)