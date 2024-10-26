import subprocess
import sys

def install(python_library):
    print(f'Installing python library: {python_library}')
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', python_library])
        if result.returncode != 0:
            print(f"Error installing {python_library}: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing {python_library}: {e}")