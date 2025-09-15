import os
import shutil

def organize_files(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("❌ Invalid folder path!")
        return

    # Loop through each item in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Skip directories, we only want to organize files
        if os.path.isdir(item_path):
            continue

        # Get the file extension
        file_ext = os.path.splitext(item)[1][1:]  # '.txt' -> 'txt'

        # Files without extension go to 'others'
        if file_ext == "":
            file_ext = "others"

        # Create a folder for this extension if it doesn't exist
        dest_folder = os.path.join(folder_path, file_ext)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        # Move the file into the folder
        shutil.move(item_path, os.path.join(dest_folder, item))
        print(f"✅ Moved {item} to {file_ext}/")

if __name__ == "__main__":
    print("📂 File Organizer Tool")
    folder = input("Enter the folder path you want to organize: ")
    organize_files(folder)
    print("✅ Files organized successfully!")
