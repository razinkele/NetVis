import webbrowser
import os

def display_html(file_path):
    # Convert to an absolute path
    absolute_path = os.path.abspath(file_path)
    
    # Open the file in the default web browser
    webbrowser.open(f"file://{absolute_path}")

# Run the test 
if __name__ == "__main__":
    # Path to your HTML file
    file_path = "network.html"
    open_html_file(file_path)
