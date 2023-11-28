import subprocess
import signal
import os.path as os

# Handle exit signal
def handler(signum, frame):
    pass

signal.signal(signal.SIGINT, handler)

file_dir = os.abspath(os.dirname(__file__))

while True:
    datamodel = input("""
                      
=================================================
============= Visualization Manager =============
=================================================
                      
 Welcome to the data visualization!
        
 Chose a data-model to visualize:
 1 - Basic (shows on shell)
 2 - Word
 3 - Line
 4 - Year

 9 - To chose all above
 0 - Exit

 Option: """)
    print("\r\n=================================================\r\n")

    if datamodel == '1':
        subprocess.run(['python', os.join(file_dir, '4_basic.py')])
    elif datamodel == '2':
        subprocess.run(os.join(file_dir, 'gword.htm'), shell=True)
    elif datamodel == '3':
        subprocess.run(os.join(file_dir, 'gline.htm'), shell=True)
    elif datamodel == '4':
        subprocess.run(os.join(file_dir, 'gline_year.htm'), shell=True)
    elif datamodel == '9':
        subprocess.run(['python', os.join(file_dir, '4_basic.py')])
        subprocess.run(os.join(file_dir, 'gword.htm'), shell=True)
        subprocess.run(os.join(file_dir, 'gline.htm'), shell=True)
        subprocess.run(os.join(file_dir, 'gline_year.htm'), shell=True)
    elif datamodel == '0':
        print(" Thank you for using our data visualizer!")
        break
    else: print("Enter a valid option.")