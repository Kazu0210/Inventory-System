import sys
import json
from PyQt6.QtWidgets import *

from pages.login_window import loginWindow
from utils.Activity_logs import Activity_Logs

def on_about_to_quit():
    print("Application is closed")
    try:
        temp_data_dir = "app/resources/data/temp_user_data.json"
        with open(temp_data_dir, 'r') as file:
            data = json.load(file)      
           
            key = list(data.keys())[0]      
            _id = data[key]
            print(f'Key: {key}, _id: {_id}')
            
            if _id:  # Check if _id is not empty
                logs = Activity_Logs()  
                logs.quit(_id)

            data = {"_id": str("")} 
        with open(temp_data_dir, 'w') as file:
            json.dump(data, file, indent=4)
    
    except FileNotFoundError:
        pass
        
def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(on_about_to_quit)
    login_window = loginWindow()
    login_window.show()  
    sys.exit(app.exec()) 
    
if __name__ == "__main__":
    main()