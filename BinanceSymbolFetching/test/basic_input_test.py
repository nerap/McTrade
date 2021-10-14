import io
import unittest
import subprocess

main_name = "BinanceBot"

class TestBasicInput(unittest.TestCase):
    def test_basic_input_00(self):
        main_stdout = subprocess.run(['python3', main_name], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_01(self):
        main_stdout = subprocess.run(['python3', main_name, '-s'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_input_02(self):
        main_stdout = subprocess.run(['python3', main_name, 's'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_03(self):
        main_stdout = subprocess.run(['python3', main_name, 'i am not existing'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_04(self):
        main_stdout = subprocess.run(['python3', main_name, 'way', 'to', 'much', 'args'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_input_05(self):
        main_stdout = subprocess.run(['python3', main_name, '--symbol'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_06(self):
        main_stdout = subprocess.run(['python3', main_name, '-h'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_07(self):
        main_stdout = subprocess.run(['python3', main_name, '--help', '-h'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -s <symbol> or --symbol=<symbol>\n')
        self.assertEqual(main_stdout, comp_stdout)

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