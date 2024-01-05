
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]) # Open a file

    if not filepath:
        return
    
    text_edit.delete("1.0", tk.END) # Clear the text widget
    with open(filepath, "r") as input_file: # Open the input file
        text = input_file.read() # Read the text from the file
        text_edit.insert(tk.END, text) # Insert the text in the text widget
    window.title(f"aPrime - {filepath}") # Set the window title

def save_file(window, text_edit):
    filepath = asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]) # Save a file

    if not filepath:
        return
    
    with open(filepath, "w") as output_file: # Open the output file
        text = text_edit.get("1.0", tk.END) # Get the text from the text widget
        output_file.write(text) # Write the text in the output file
    window.title(f"aPrime - {filepath}") # Set the window title

def main():
    window = tk.Tk()  # Create a window
    window.title("Text Editor")  # Set a title

    # Configure the window's layout
    window.columnconfigure(0, minsize=800, weight=1)  # Set the column configuration for text widget
    window.rowconfigure(1, minsize=800, weight=1)  # Set the row configuration for text widget

    # Create a text widget
    text_edit = tk.Text(window, font="helvetica 13")
    text_edit.grid(row=1, column=0, sticky="nsew")  # Place the text widget

    # Create a frame for buttons
    frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    frame.grid(row=0, column=0, sticky="ew")  # Place the frame at the top

    # Create and place the "Open" button
    button_open = tk.Button(frame, text="Open", command=lambda: open_file(window, text_edit))
    button_open.pack(side=tk.LEFT, padx=5, pady=5)

    # Create and place the "Save" button
    button_save = tk.Button(frame, text="Save", command=lambda: save_file(window, text_edit))
    button_save.pack(side=tk.LEFT, padx=5)

    # keyboard shortcuts
    window.bind("<Control-o>", lambda event: open_file(window, text_edit))
    window.bind("<Control-s>", lambda event: save_file(window, text_edit))

    window.mainloop()  # Keep the window open


main()  # Call the main function   
