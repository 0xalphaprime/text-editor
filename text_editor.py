
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re
import webbrowser

headline_color = "#FFA07A"  # headline color
bold_color = "#4287f5"  # bold text color
italics_color = "#42f5d4"  # italic text color
inline_code_color = "#797d7c"  # inline code color


def open_file(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]) # Open a file

    if not filepath:
        return
    
    text_edit.delete("1.0", tk.END) # Clear the text widget
    with open(filepath, "r") as input_file: # Open the input file
        text = input_file.read() # Read the text from the file
        text_edit.insert(tk.END, text) # Insert the text in the text widget
        apply_markdown_formatting(text_edit)  # Apply Markdown formatting to the loaded text
    window.title(f"aPrime - {filepath}") # Set the window title


def save_file(window, text_edit):
    filepath = asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md")]) # Save a file

    if not filepath:
        return
    
    with open(filepath, "w") as output_file: # Open the output file
        text = text_edit.get("1.0", tk.END) # Get the text from the text widget
        output_file.write(text) # Write the text in the output file
    window.title(f"aPrime - {filepath}") # Set the window title

def apply_markdown_formatting(text_widget):
    """
    Apply Markdown formatting to the text in the text widget.
    Now includes different font sizes and colors for headlines.
    """
    text = text_widget.get("1.0", tk.END)

    # Remove existing tags
    text_widget.tag_remove("bold", "1.0", tk.END)
    text_widget.tag_remove("italic", "1.0", tk.END)
    for i in range(1, 6):
        text_widget.tag_remove(f"h{i}", "1.0", tk.END)

    # Formatting for bold text
    for match in re.finditer(r"\*\*(.*?)\*\*", text):
        start, end = match.span()
        text_widget.tag_add("bold", f"1.0+{start}c", f"1.0+{end}c")
        text_widget.tag_config("bold", font=("helvetica", 13, "bold"), foreground=bold_color)  # Blue color for bold text

    # Formatting for italic text
    for match in re.finditer(r"\*(.*?)\*", text):
        start, end = match.span()
        text_widget.tag_add("italic", f"1.0+{start}c", f"1.0+{end}c")
        text_widget.tag_config("italic", font=("helvetica", 13, "italic"), foreground=italics_color)  # Green color for italic text

    # Formatting for headlines
    for match in re.finditer(r"^(#{1,5})\s+(.*)", text, re.MULTILINE):
        hash_count = len(match.group(1))  # Number of # characters
        start, end = match.span()  # Get the span of the entire headline including '#'
        
        # Define font size based on the hash_count
        font_size = 22 - (hash_count * 2)

        tag_name = f"h{hash_count}"
        text_widget.tag_add(tag_name, f"1.0+{start}c", f"1.0+{end}c")
        text_widget.tag_config(tag_name, font=("helvetica", font_size, "bold"), foreground=headline_color)

     # Formatting for inline code (single backticks)
    for match in re.finditer(r"`(.*?)`", text):
        start, end = match.span(1)  # Adjusted to get only the text within backticks
        text_widget.tag_add("inline_code", f"1.0+{start}c", f"1.0+{end}c")
        text_widget.tag_config("inline_code", font=("Courier", 12), background=inline_code_color)

    # Formatting for fenced code blocks (triple backticks)
    for match in re.finditer(r"```.*?\n(.*?)```", text, re.DOTALL):
        code_start, code_end = match.span(1)  # Adjusted to get only the text within triple backticks, after the first newline
        text_widget.tag_add("block_code", f"1.0+{code_start}c", f"1.0+{code_end}c")
        text_widget.tag_config("block_code", font=("Courier", 12), background=inline_code_color)

    
   


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

    text_edit.bind("<KeyRelease>", lambda event: apply_markdown_formatting(text_edit))

    window.mainloop()  # Keep the window open


main()  # Call the main function   
