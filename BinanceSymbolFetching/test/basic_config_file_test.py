import io
import unittest
import subprocess

directory = "BinanceSymbolFetching/"
main_name = directory + "configuration_file_parsing.py"

class TestBasicConfigFile(unittest.TestCase):

    def test_basic_config_file_00(self):
        main_stdout = subprocess.run(['python3', main_name, 'f', 'file/doesnt/exist'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_01(self):
        main_stdout = subprocess.run(['python3', main_name, '-f', 'ETGGGGdfs'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: can\'t open ETGGGGdfs\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_config_file_02(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=ETGGGGdfs'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: can\'t open ETGGGGdfs\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_03(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=', 'ETGGGGdfs'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: configuration file missing\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_config_file_05(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_duplicate'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: duplicated symbol BTCUSDT in configuration file\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_06(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_empty'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode(directory + 'test/test_config_file/config_file_empty is not a valid config file\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_07(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_empty_symbols'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: your configuration file is empty\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_config_file_08(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_json_empty'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: configuration file doesn\'t have the right key\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_09(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_wrong_format'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode(directory + 'test/test_config_file/config_file_wrong_format is not a valid config file\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_09(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_wrong_key'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: configuration file doesn\'t have the right key\n')
        self.assertEqual(main_stdout, comp_stdout)

if __name__ == '__main__':
    unittest.main()