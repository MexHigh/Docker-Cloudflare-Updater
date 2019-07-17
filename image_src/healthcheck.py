import psutil
import sys

for process in psutil.process_iter():
    if process.cmdline() == ['python3', 'cfupdater.py']:
         print("0")
         sys.exit(0)

print("1")
sys.exit(1)
