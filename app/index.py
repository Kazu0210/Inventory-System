import sys, json
from pathlib import Path
from PyQt6.QtWidgets import *

from src.pages.login_window import loginWindow
from src.utils.Activity_logs import Activity_Logs

def on_about_to_quit():
    # Define the relative path to the file
    relative_path = Path("app/resources/data/temp_user_data.json")

    # Get the absolute path (relative to the current working directory)
    temp_data_dir = Path.cwd() / relative_path

    if not temp_data_dir.exists():
        print(f"The file {temp_data_dir} does not exist.")
    else:
        print(f"File path: {temp_data_dir}")

    try:
        with open(temp_data_dir, 'r') as file:
            data = json.load(file)

        # Accessing the first key efficiently
        key = next(iter(data))  # More efficient than list(data.keys())[0]
        _id = data[key]

        print(f'Key: {key}, _id: {_id}')

        if _id:  # Check if _id is not empty
            logs = Activity_Logs()  
            logs.quit(_id)

        # Update the data efficiently
        data[key] = {""}  # Assuming you want to reset the _id value for the same key

        # Write back the modified data
        with open(temp_data_dir, 'w') as file:
            json.dump(data, file, indent=4)

    except FileNotFoundError:
        print(f"Error: The file '{temp_data_dir}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{temp_data_dir}'.")
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