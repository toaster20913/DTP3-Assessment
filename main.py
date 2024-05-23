import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import platform


def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_var.set(directory_path)
        update_file_list(directory_path)

def update_file_list(directory_path):
    file_list.delete(0, tk.END)
    for filename in os.listdir(directory_path):
        if filename.endswith(file_extension_var.get()):
            file_list.insert(tk.END, filename)

def apply_filter():
    directory_path = directory_var.get()
    if directory_path:
        update_file_list(directory_path)

def open_file(event):
    selection = file_list.curselection()
    if selection:
        filename = file_list.get(selection[0])
        file_path = os.path.join(directory_var.get(), filename)
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            else:  # linux variants
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

# Create the main window
root = tk.Tk()
root.title("Results Checker")

# Frame for directory selection
directory_frame = tk.Frame(root)
directory_frame.pack(pady=10)

directory_label = tk.Label(directory_frame, text="Select Directory:")
directory_label.grid(row=0, column=0)

directory_var = tk.StringVar()
directory_entry = tk.Entry(directory_frame, textvariable=directory_var, width=50)
directory_entry.grid(row=0, column=1)

browse_button = tk.Button(directory_frame, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2)

# Frame for file extension filter
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

file_extension_label = tk.Label(filter_frame, text="File Extension:")
file_extension_label.grid(row=0, column=0)

file_extension_var = tk.StringVar(value=".txt")
file_extension_entry = tk.Entry(filter_frame, textvariable=file_extension_var, width=10)
file_extension_entry.grid(row=0, column=1)

apply_filter_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filter)
apply_filter_button.grid(row=0, column=2)

# Frame for file list
file_list_frame = tk.Frame(root)
file_list_frame.pack(pady=10)

file_list_label = tk.Label(file_list_frame, text="Files:")
file_list_label.pack()

file_list = tk.Listbox(file_list_frame, width=50)
file_list.pack()

# Bind double-click event to open the file
file_list.bind('<Double-1>', open_file)

root.mainloop()
