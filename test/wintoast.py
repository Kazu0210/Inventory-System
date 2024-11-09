from win10toast import ToastNotifier

def send_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5)

# Usage
send_notification("Enable Auto Backup", "Auto Backup enabled for the scheduled task.")
