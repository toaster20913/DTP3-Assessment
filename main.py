import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Toplevel, StringVar
import customtkinter as ctk

# Username: username
# Password: password

# Set the initial theme to dark mode
current_mode = "dark"
ctk.set_appearance_mode(current_mode)  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Function to check login
def check_login():
    if username_var.get().strip() == "username" and password_var.get().strip() == "password":
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
    for filename in os.listdir(directory_path):
        if filter_text in filename.lower():
            file_list.insert('end', filename)

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
    points = 9 - placement
    return max(points, 1)  # Ensure minimum points is 1

# Function to check files and calculate points for clubs
def check_files_and_assign_points():
    directory_path = directory_var.get()
    if not directory_path:
        messagebox.showerror("Error", "No directory selected")
        return

    club_points = {}

    for filename in os.listdir(directory_path):
        if name_filter_var.get().lower() in filename.lower():
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
                for i, line in enumerate(lines[1:9]):  # Only consider lines 2 to 9 (1-indexed)
                    columns = line.split(',')
                    if len(columns) > 5:
                        club_name = columns[5].strip()  # Using the 6th column for club names
                        points = assign_points(i + 1)
                        print(f"Processing line {i+1}: Club {club_name}, Placement {i+1}, Points {points}")  # Debugging print
                        if club_name in club_points:
                            club_points[club_name] += points
                        else:
                            club_points[club_name] = points
            except Exception as e:
                messagebox.showerror("Error", f"Error processing file {filename}: {e}")
                return

    # Display the results
    display_results(club_points)

# Function to display results in a new window
def display_results(club_points):
    results_window = Toplevel(root)
    results_window.title("Results")

    results_frame = ctk.CTkFrame(results_window)
    results_frame.pack(pady=10, padx=10, fill='both', expand=True)

    scrollbar = Scrollbar(results_frame, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    results_listbox = Listbox(results_frame, yscrollcommand=scrollbar.set, width=50, height=20)
    results_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=results_listbox.yview)

    sorted_clubs = sorted(club_points.items(), key=lambda item: item[1], reverse=True)

    # Highlight the club with the most points
    if sorted_clubs:
        top_club = sorted_clubs[0]
        results_listbox.insert('end', f"Top Club: {top_club[0]} with {top_club[1]} points")

    for i, (club, points) in enumerate(sorted_clubs):
        results_listbox.insert('end', f"{i+1}. {club}: {points} points")

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

# Frame for buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

# Button to check files and assign points
check_files_button = ctk.CTkButton(button_frame, text="Results", command=check_files_and_assign_points)
check_files_button.grid(row=0, column=0, padx=5)

# Button to toggle between dark mode and light mode (Main Window)
toggle_mode_button_main = ctk.CTkButton(button_frame, text="Toggle Dark/Light Mode", command=toggle_mode)
toggle_mode_button_main.grid(row=0, column=1, padx=5)

# Run the application
root.mainloop()
