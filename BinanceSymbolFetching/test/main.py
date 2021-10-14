import io
import unittest
import subprocess

main_name = "main.py"

class TestBinanceBot(unittest.TestCase):
    def test_basic_input_00(self):
        main_stdout = subprocess.run(['python3', main_name], stdout=subprocess.PIPE).stdout
        comp_stdout = str.encode("python3 main.py -s <symbol> or --symbol=<symbol>\npython3 main.py -h or --help\n")
        self.assertEqual(main_stdout, comp_stdout)

if __name__ == '__main__':
    unittest.main()