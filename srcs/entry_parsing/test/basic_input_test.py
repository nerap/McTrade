import io
import unittest
import subprocess

main_name = "McTrade.py"

class TestBasicInput(unittest.TestCase):
    def test_basic_input_00(self):
        main_stdout = subprocess.run(['python3', main_name], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_01(self):
        main_stdout = subprocess.run(['python3', main_name, '-f'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_input_02(self):
        main_stdout = subprocess.run(['python3', main_name, 'f'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_03(self):
        main_stdout = subprocess.run(['python3', main_name, 'i am not existing'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_04(self):
        main_stdout = subprocess.run(['python3', main_name, 'way', 'to', 'much', 'args'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)
    
    def test_basic_input_05(self):
        main_stdout = subprocess.run(['python3', main_name, '--file'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\npython3 ' + main_name + ' -h or --help\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_06(self):
        main_stdout = subprocess.run(['python3', main_name, '-h'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\n')
        self.assertEqual(main_stdout, comp_stdout)

    def test_basic_input_07(self):
        main_stdout = subprocess.run(['python3', main_name, '--help', '-h'], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode('python3 ' + main_name + ' -f <file> or --file=<file>\n')
        self.assertEqual(main_stdout, comp_stdout)

if __name__ == '__main__':
    unittest.main()