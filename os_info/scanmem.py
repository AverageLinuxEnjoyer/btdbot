import pexpect
import time
from logger import log


class MemoryScanner:
    def __init__(self, start_money=850, first_round=1):
        self.start_money = 850
        self.first_round = 1

        self.process = pexpect.spawn("scanmem")
        self.process.expect("scanmem version")
        self.process.sendline(f"pid {self.__get_pid()}")
        self.process.expect("info: maps file located")

        self.process.sendline("option scan_data_type float64")
        self.process.expect('>')

    def __get_pid(self):
        import subprocess

        bloons_path = r"Z:\home\nullptr\.local"

        output = subprocess.check_output(
            'ps aux | grep BloonsTD6.exe', shell=True)

        output = str(output)

        end = output.find("Z:")
        output = output[end-100:end]
        beg = output.find("nullptr")

        user = output.find("nullptr")
        
        log("BloonsTD6.exe process id found.")
        return output[user:].split()[1]

    def locate_money(self, value=850):
        self.process.sendline(str(value))
        self.process.expect(r'info: we currently have \d+ matches.')
        matches = int(''.join(filter(str.isdigit, str(self.process.after))))

        if matches > 1:
            log(f"{matches} possible money addresses found.")
            return False
        elif matches == 1:
            log("Money address found.")
            return True
        else:
            log("Money adress couldn't be found.")

    def get_money(self):
        self.process.sendline("update")
        self.process.expect(".ok")
        self.process.sendline("list")
        self.process.expect("F64")

        return int(float(str(self.process.before).split(',')[-2]))
