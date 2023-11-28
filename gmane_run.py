import subprocess
import signal
import os


# Handle exit signal
def handler(signum, frame):
    pass

signal.signal(signal.SIGINT, handler)


def file_path(*path:str) -> str:
    return os.path.join(*path)


def initial_input() -> int:
    while True:
        initial = input("""
                        
==============================================
============= Aplication Manager =============
==============================================
                        
 Welcome to the aplication manager!
                        
 Wich application you want to run:
 1 - Spider (search the web for the emails)
 2 - Model (make an eficient database model from the 'spider' database)
 3 - Data Visualization

 0 - Exit

 Option: """)
        print("\r\n==============================================\r\n")
        try: 
            initial = int(initial)
        except:
            print("Please enter a valid option.")
            continue

        if initial < 0 or initial > 3:
            print("Please enter a valid option.")
            continue
        return initial



while True:
    file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))
    option = initial_input()

    if option == 1:
        subprocess.run(['python', file_path(file_dir, "1_spider.py")])
    elif option == 2:
        subprocess.run(['python', file_path(file_dir, "2_model.py")])
    elif option == 3:
        subprocess.run(['python', file_path(file_dir, '3_visualization.py')])
    elif option == 0:
        input(" Thanks for using the manager!\r\n\r\n Press 'Enter'")
        break