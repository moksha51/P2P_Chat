# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Client
import Server
import subprocess
import time

subprocess.run(["python", "Server.py"])
print('Running Server')
time.sleep(2)
subprocess.run(["python", "Client.py"])
subprocess.run(["python", "Client.py"])
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
