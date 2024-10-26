import win32com.client

def print_word_document(file_path):
    # Initialize Word application
    word_app = win32com.client.Dispatch("Word.Application")
    word_app.Visible = False

    # Open the document
    doc = word_app.Documents.Open(file_path)

    # Print the document
    doc.PrintOut()

    # Close the document
    doc.Close(False)
    word_app.Quit()

# Replace 'your_file.docx' with your actual file path
file_path = "your_file.docx"
print_word_document(file_path)