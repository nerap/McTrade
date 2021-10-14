import io
import unittest
import subprocess

main_name = "BinanceBot"

class TestBasicConfigFile(unittest.TestCase):

    def test_basic_input_08(self):
        main_stdout = subprocess.run(['python3', main_name, '-s', 'ETGGGG'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Symbol is not valid for BinanceBot check your parameters\nInvalid symbol.\nReturn Code : -1121\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_09(self):
        main_stdout = subprocess.run(['python3', main_name, '-s', 'ETGGGGdfs'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Symbol is not valid for BinanceBot check your parameters\nIllegal characters found in parameter \'symbol\'; legal range is \'^[A-Z0-9-_.]{1,20}$\'.\nReturn Code : -1100\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_input_10(self):
        main_stdout = subprocess.run(['python3', main_name, '--symbol=ETGGGGdfs'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Symbol is not valid for BinanceBot check your parameters\nIllegal characters found in parameter \'symbol\'; legal range is \'^[A-Z0-9-_.]{1,20}$\'.\nReturn Code : -1100\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_11(self):
        main_stdout = subprocess.run(['python3', main_name, '--symbol=', 'ETGGGGdfs'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('Symbol is not valid for BinanceBot check your parameters\nParameter \'symbol\' was empty.\nReturn Code : -1105\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_12(self):
        main_stdout = subprocess.run(['python3', main_name, '--symbol=LINKBTC'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('LINKBTC\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_input_13(self):
        main_stdout = subprocess.run(['python3', main_name, '-s', 'LINKBTC'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('LINKBTC\n')
        self.assertEqual(main_stdout, comp_stdout)

if __name__ == '__main__':
    unittest.main()