import io
import unittest
import subprocess

directory = "srcs/entry_parsing/"
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

    def test_basic_config_file_04(self):
        main_stdout = subprocess.run(['python3', main_name, '-f', directory + 'test/test_config_file/config_file_wrong_currency.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: XRPEUR is not valid for BinanceBot check your configuration file\nBinanceBot can only hold USDT currency as pair with another crypto like -> BTCUSDT, XRPUSDT, ETHUSDT, etc..\nNote that you cannot trade USDT currency such as -> USDTBIDR, USDTRUB, USDTUAH, etc..\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_config_file_05(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_duplicate.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: duplicated symbol ETHUSDT in configuration file\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_06(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_empty.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: can\'t parse ' + directory + 'test/test_config_file/config_file_empty.conf\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_07(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_empty_symbols.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: NOSYMBOL is not valid for BinanceBot check your configuration file\nBinanceBot can only hold USDT currency as pair with another crypto like -> BTCUSDT, XRPUSDT, ETHUSDT, etc..\nNote that you cannot trade USDT currency such as -> USDTBIDR, USDTRUB, USDTUAH, etc..\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_config_file_08(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_nginx_empty.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: NOSYMBOL is not valid for BinanceBot check your configuration file\nBinanceBot can only hold USDT currency as pair with another crypto like -> BTCUSDT, XRPUSDT, ETHUSDT, etc..\nNote that you cannot trade USDT currency such as -> USDTBIDR, USDTRUB, USDTUAH, etc..\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_09(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_wrong_format.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Error: can\'t parse ' + directory + 'test/test_config_file/config_file_wrong_format.conf\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_config_file_09(self):
        main_stdout = subprocess.run(['python3', main_name, '--file=' + directory + 'test/test_config_file/config_file_wrong_key.conf'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('[\'WRONG_KEY\'] is not valid for BinanceBot check your configuration file\n')
        self.assertEqual(main_stdout, comp_stdout)

if __name__ == '__main__':
    unittest.main()