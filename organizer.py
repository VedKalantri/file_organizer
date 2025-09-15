import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import json
from datetime import datetime
import threading
import time

# Setup logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/organize_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

UNDO_FILE = "undo_data.txt"

def save_undo(data):
    with open(UNDO_FILE, "w") as f:
        json.dump(data, f)

def load_undo():
    if os.path.exists(UNDO_FILE):
        with open(UNDO_FILE, "r") as f:
            return json.load(f)
    return None

def clear_undo():
    if os.path.exists(UNDO_FILE):
        os.remove(UNDO_FILE)

def organize_files(folder_path):
    try:
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Invalid folder path!")
            return

        undo_data = {"folder": folder_path, "files": []}
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

            dest_path = os.path.join(dest_folder, item)
            shutil.move(item_path, dest_path)
            files_moved += 1

            # Save for undo
            undo_data["files"].append({"src": dest_path, "dest": item_path})

            # Log the operation
            logging.info(f"Moved {item} to {file_ext}/")

        if files_moved == 0:
            messagebox.showinfo("Info", "No files to organize.")
            return

        save_undo(undo_data)
        messagebox.showinfo("Success", f"Files organized successfully!\nTotal files moved: {files_moved}")

    except PermissionError:
        messagebox.showerror("Permission Error", "You don't have permission to access this folder.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")


def undo_organize():
    data = load_undo()
    if not data:
        messagebox.showinfo("Info", "Nothing to undo.")
        return

    folder = data["folder"]
    files = data["files"]
    undone = 0

    try:
        for file in files:
            if os.path.exists(file["src"]):
                shutil.move(file["src"], file["dest"])
                undone += 1
                logging.info(f"Undo: Moved {os.path.basename(file['src'])} back")

        clear_undo()
        messagebox.showinfo("Undo", f"Undo successful! {undone} files moved back.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during undo:\n{str(e)}")


def schedule_task(interval_hours):
    def task():
        while True:
            folder = folder_path.get()
            if folder:
                organize_files(folder)
            time.sleep(interval_hours * 3600)

    t = threading.Thread(target=task, daemon=True)
    t.start()
    messagebox.showinfo("Scheduled", f"Task scheduled every {interval_hours} hours.")


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)


def start_organizing():
    folder = folder_path.get()
    organize_files(folder)


def start_undo():
    undo_organize()


def schedule_daily():
    schedule_task(24)


def schedule_weekly():
    schedule_task(24 * 7)


# GUI setup
root = tk.Tk()
root.title("Advanced File Organizer")
root.geometry("450x300")
root.resizable(False, False)

folder_path = tk.StringVar()

tk.Label(root, text="📂 File Organizer", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Entry(frame, textvariable=folder_path, width=40).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Browse", command=browse_folder).pack(side=tk.LEFT)

tk.Button(root, text="Organize Files", command=start_organizing, width=20, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Undo Last Organize", command=start_undo, width=20, bg="orange", fg="white").pack(pady=5)
tk.Button(root, text="Schedule Daily", command=schedule_daily, width=20, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Schedule Weekly", command=schedule_weekly, width=20, bg="blue", fg="white").pack(pady=5)

root.mainloop()
