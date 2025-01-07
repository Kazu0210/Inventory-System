import subprocess
from plyer import notification

# Function to show notification
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification will disappear after 10 seconds
    )

# Remove the dist and build directories
try:
    subprocess.run(['rmdir', '/s', '/q', 'dist'], shell=True, check=True)
    subprocess.run(['rmdir', '/s', '/q', 'build'], shell=True, check=True)
    show_notification("Success", "dist and build directories removed successfully.")
except subprocess.CalledProcessError:
    show_notification("Error", "Failed to remove dist or build directories.")

# Run pyinstaller with the index.spec file
try:
    subprocess.run(['pyinstaller', 'index.spec'], check=True)
    show_notification("Success", "PyInstaller ran successfully.")
except subprocess.CalledProcessError:
    show_notification("Error", "PyInstaller failed.")