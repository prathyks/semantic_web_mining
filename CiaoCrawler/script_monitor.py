import subprocess
import logging

logging.basicConfig(filename='crawler.log', level=logging.WARN)


def read_file():
    f = open('last_date', 'r')
    date_s = f.readline()
    f.close()
    return date_s

while True:
    #date_str = read_file()
    #subprocess.call(["python3.4", "testSQL.py", date_str])
    subprocess.call(["python3.4", "scan_friends.py"])
    logging.warn("Restarting........................")