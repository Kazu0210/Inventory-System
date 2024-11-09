import threading
from plyer import notification

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5  # Notification duration in seconds
    )

def handle_notifications():
    # Create threads to send notifications concurrently
    thread1 = threading.Thread(target=send_notification, args=("Enable Auto Backup", "Auto Backup enabled for the scheduled task."))
    thread2 = threading.Thread(target=send_notification, args=("Backup Status", "Backup is running."))
    thread3 = threading.Thread(target=send_notification, args=("Backup Completed", "Backup process completed successfully."))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

# Call the function to send notifications
handle_notifications()
