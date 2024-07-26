import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, StringVar
import customtkinter as ctk
import csv

# Username: username
# Password: password

# Set the initial theme to dark mode
current_mode = "dark"
ctk.set_appearance_mode(current_mode)  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Function to check login
def check_login():
    username = username_var.get().strip()
    password = password_var.get().strip()

    if len(password) > 15:
        messagebox.showerror("Error", "Password is too long (maximum 15 characters)")
        return

    if username == "username" and password == "password":
        login_window.destroy()
        root.deiconify()  # Show the main window
    else:
        messagebox.showerror("Error", "Invalid username or password")


# Function to browse directory
def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_var.set(directory_path)
        update_file_list(directory_path)

# Function to update file list based on selected directory and file name filter
def update_file_list(directory_path):
    file_list.delete(0, 'end')
    filter_text = name_filter_var.get().lower()
    count = 0  # Initialize file count
    for filename in os.listdir(directory_path):
        if filter_text in filename.lower():
            file_list.insert('end', filename)
            count += 1  # Increment file count
    file_count_var.set(f"File Count: {count}")  # Update file count display

# Function to apply name filter
def apply_filter():
    directory_path = directory_var.get()
    if directory_path:
        update_file_list(directory_path)

# Function to open file (platform-dependent)
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

# Function to assign points based on placement
def assign_points(placement):
    if placement <= 0:  # No points for DQ or DNS (placement <= 0)
        return 0
    points = 9 - placement
    return max(points, 1)  # Ensure minimum points is 1

def check_files_and_assign_points():
    directory_path = directory_var.get()
    if not directory_path:
        messagebox.showerror("Error", "No directory selected")
        return

    club_points = {}

    for filename in os.listdir(directory_path):
        if name_filter_var.get().lower() in filename.lower():
            current_file_var.set(f"Processing file: {filename}")
            root.update_idletasks()  # Force update the GUI

            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        lines = file.readlines()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read file {filename}: {e}")
                    return

            try:
                for i, line in enumerate(lines[1:]):
                    columns = line.split(',')
                    if len(columns) > 5:
                        club_name = columns[5].strip()  # Using the 6th column for club names
                        if not club_name or club_name.upper() in ["DQ", "DNS"]:
                            continue  # Skip empty names, DQ, or DNS entries
                        points = assign_points(i + 1)
                        if club_name in club_points:
                            club_points[club_name] += points
                        else:
                            club_points[club_name] = points
                    else:
                        print(f"Line {i+1} is missing columns: {line.strip()}")
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file {filename}: {e}")
                return

    # Clear the current file label after processing
    current_file_var.set("Processing complete.")
    root.update_idletasks()  # Ensure the final update to the GUI

    # Write results to a CSV file
    save_results_to_txt(club_points)


def save_results_to_txt(club_points):
    results_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not results_file_path:
        return

    try:
        with open(results_file_path, 'w', newline='', encoding='utf-8') as txtfile:
            sorted_clubs = sorted(club_points.items(), key=lambda item: item[1], reverse=True)
            for club, points in sorted_clubs:
                txtfile.write(f'{club},{points}\n')

        messagebox.showinfo("Success", f"Results saved to {results_file_path}")

        # Automatically open the file in Notepad
        if platform.system() == 'Windows':
            os.startfile(results_file_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', results_file_path))
        else:  # linux variants
            subprocess.call(('xdg-open', results_file_path))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save results: {e}")

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

# Button to toggle between dark mode and light mode (Login Window)
toggle_mode_button_login = ctk.CTkButton(login_window, text="Toggle Dark/Light Mode", command=toggle_mode)
toggle_mode_button_login.grid(row=3, column=0, columnspan=2, pady=10)

# Frame for directory selection
directory_frame = ctk.CTkFrame(root)
directory_frame.pack(pady=10)

directory_label = ctk.CTkLabel(directory_frame, text="Select Directory:")
directory_label.grid(row=0, column=0)

directory_var = StringVar()
directory_entry = ctk.CTkEntry(directory_frame, textvariable=directory_var, width=500)
directory_entry.grid(row=0, column=1, padx=10)

browse_button = ctk.CTkButton(directory_frame, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2)

# Frame for name filter
filter_frame = ctk.CTkFrame(root)
filter_frame.pack(pady=10)

name_filter_label = ctk.CTkLabel(filter_frame, text="File Name Filter:")
name_filter_label.grid(row=0, column=0)

name_filter_var = StringVar(value="")
name_filter_entry = ctk.CTkEntry(filter_frame, textvariable=name_filter_var, width=500)
name_filter_entry.grid(row=0, column=1, padx=10)

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

# Frame for file count
file_count_frame = ctk.CTkFrame(root)
file_count_frame.pack(pady=10)

file_count_var = StringVar(value="File Count: 0")
file_count_label = ctk.CTkLabel(file_count_frame, textvariable=file_count_var)
file_count_label.pack()

# Frame for buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

# Button to check files and assign points
check_files_button = ctk.CTkButton(button_frame, text="Results", command=check_files_and_assign_points)
check_files_button.grid(row=0, column=0, padx=5)

# Button to toggle between dark mode and light mode (Main Window)
toggle_mode_button_main = ctk.CTkButton(button_frame, text="Toggle Dark/Light Mode", command=toggle_mode)
toggle_mode_button_main.grid(row=0, column=1, padx=5)

# Frame for current file being processed
current_file_frame = ctk.CTkFrame(root)
current_file_frame.pack(pady=10)

current_file_var = StringVar(value="No file being processed")
current_file_label = ctk.CTkLabel(current_file_frame, textvariable=current_file_var)
current_file_label.pack()

# Run the application
root.mainloop()
