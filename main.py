import os
import platform
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Toplevel, StringVar

#Username: username
#Password: password


# Set the theme (optional)
current_mode = "dark"
ctk.set_appearance_mode(current_mode)  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

def check_login():
    if username_var.get() == "username" and password_var.get() == "password":
        login_window.destroy()
        root.deiconify()  # Show the main window
    else:
        messagebox.showerror("Error", "Invalid username or password")

def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_var.set(directory_path)
        update_file_list(directory_path)

def update_file_list(directory_path):
    file_list.delete(0, 'end')
    filter_text = filter_var.get().lower()
    for filename in os.listdir(directory_path):
        if filter_text in filename.lower():
            file_list.insert('end', filename)

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


# Function to toggle between dark mode and light mode
def toggle_mode():
    global current_mode
    if current_mode == "dark":
        ctk.set_appearance_mode("light")
        current_mode = "light"
    else:
        ctk.set_appearance_mode("dark")
        current_mode = "dark"

# Create the main window
root = ctk.CTk()
root.title("Results Checker")
root.withdraw()  # Hide the main window initially


# Create the login window
login_window = ctk.CTkToplevel(root)
login_window.title("Login")

username_label = ctk.CTkLabel(login_window, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)

username_var = StringVar()
username_entry = ctk.CTkEntry(login_window, textvariable=username_var)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ctk.CTkLabel(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_var = StringVar()
password_entry = ctk.CTkEntry(login_window, textvariable=password_var, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = ctk.CTkButton(login_window, text="Login", command=check_login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Frame for directory selection
directory_frame = ctk.CTkFrame(root)
directory_frame.pack(pady=10)

directory_label = ctk.CTkLabel(directory_frame, text="Select Directory:")
directory_label.grid(row=0, column=0)

directory_var = StringVar()
directory_entry = ctk.CTkEntry(directory_frame, textvariable=directory_var, width=350)
directory_entry.grid(row=0, column=1, padx=10)

browse_button = ctk.CTkButton(directory_frame, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2)

# Frame for file name filter
filter_frame = ctk.CTkFrame(root)
filter_frame.pack(pady=10)

filter_label = ctk.CTkLabel(filter_frame, text="Filter by Name:")
filter_label.grid(row=0, column=0)

filter_var = StringVar(value="")
filter_entry = ctk.CTkEntry(filter_frame, textvariable=filter_var, width=100)
filter_entry.grid(row=0, column=1, padx=10)

apply_filter_button = ctk.CTkButton(filter_frame, text="Apply Filter", command=apply_filter)
apply_filter_button.grid(row=0, column=2)

# Frame for file list
file_list_frame = ctk.CTkFrame(root)
file_list_frame.pack(pady=10)

file_list_label = ctk.CTkLabel(file_list_frame, text="Files:")
file_list_label.pack()

# Create a scrollbar and attach it to the file list
scrollbar = Scrollbar(file_list_frame, orient='vertical')

# Define file_list using Tkinter's Listbox
file_list = Listbox(file_list_frame, width=100, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=file_list.yview)
scrollbar.pack(side='right', fill='y')
file_list.pack(side='left', fill='both', expand=True)

# Bind double-click event to open the file
file_list.bind('<Double-1>', open_file)

# Button to toggle between dark and light modes
mode_button = ctk.CTkButton(root, text="Toggle Dark/Light Mode", command=toggle_mode)
mode_button.pack(pady=10)


# Button to toggle between dark mode and light mode (Login Window)
toggle_mode_button_login = ctk.CTkButton(login_window, text="Toggle Dark/Light Mode", command=toggle_mode)
toggle_mode_button_login.grid(row=3, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
