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
============== Visualization Model ==============
=================================================
                      
 Welcome to the data visualization creation!
        
 Chose a data-model to generate:
 1 - Basic (shows on shell)
 2 - Word
 3 - Line
 4 - Year

 5 - To chose all above

 9 - Visualize data (default browser)
 0 - Exit

 Option: """)
    print("\r\n=================================================\r\n")

    if datamodel == '1':
        subprocess.run(['python', os.join(file_dir, '4_basic.thon')])
    elif datamodel == '2':
        subprocess.run(['python', os.join(file_dir, '4_word.py')])
    elif datamodel == '3':
        subprocess.run(['python', os.join(file_dir, '4_line.py')])
    elif datamodel == '4':
        subprocess.run(['python', os.join(file_dir, '4_year.py')])
    elif datamodel == '5':
        subprocess.run(['python', os.join(file_dir, '4_basic.py')])
        subprocess.run(['python', os.join(file_dir, '4_word.py')])
        subprocess.run(['python', os.join(file_dir, '4_line.py')])
        subprocess.run(['python', os.join(file_dir, '4_year.py')])
    elif datamodel == '9':
        subprocess.run(['python', os.join(file_dir, '5_visualization_on_browser.py')])
    elif datamodel == '0':
        print(" Thank you for using our data-model creator!")
        break
    else: print("Enter a valid option.")