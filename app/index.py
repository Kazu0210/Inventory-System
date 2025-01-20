import sys, json
from pathlib import Path
from PyQt6.QtWidgets import *

from src.pages.login_window import loginWindow
from src.utils.Activity_logs import Activity_Logs
from src.utils.Logs import Logs

def on_about_to_quit():
    try:
        logs = Logs()
        logs.record_log(event='login_closed')
    except Exception as e:
        print(f"An error occurred: {e}")
        
def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(on_about_to_quit)
    login_window = loginWindow()
    login_window.show()  
    sys.exit(app.exec())    
    
if __name__ == "__main__":
    main()