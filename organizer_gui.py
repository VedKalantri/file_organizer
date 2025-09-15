import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def organize_files(folder_path):
    try:
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Invalid folder path!")
            return

        files_moved = 0

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                continue

            file_ext = os.path.splitext(item)[1][1:]

            if file_ext == "":
                file_ext = "others"

            dest_folder = os.path.join(folder_path, file_ext)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            shutil.move(item_path, os.path.join(dest_folder, item))
            files_moved += 1

        messagebox.showinfo("Success", f"Files organized successfully!\nTotal files moved: {files_moved}")

    except PermissionError:
        messagebox.showerror("Permission Error", "You don't have permission to access this folder.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)


def start_organizing():
    folder = folder_path.get()
    organize_files(folder)


# GUI setup
root = tk.Tk()
root.title("File Organizer")
root.geometry("400x200")
root.resizable(False, False)

folder_path = tk.StringVar()

# Title Label
title_label = tk.Label(root, text="📂 File Organizer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Folder selection
frame = tk.Frame(root)
frame.pack(pady=5)

entry = tk.Entry(frame, textvariable=folder_path, width=40)
entry.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

# Organize Button
organize_button = tk.Button(root, text="Organize Files", command=start_organizing, width=20, bg="green", fg="white")
organize_button.pack(pady=20)

# Run the GUI
root.mainloop()
