import subprocess

# Command to scan using scanimage
subprocess.run(["scanimage", "--resolution", "300", "--mode", "Color", "--format", "png", "--output-file", "scanned_image.png"])
print("Image saved as scanned_image.png")
