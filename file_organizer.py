import os
import shutil


# File categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
    "Programs": [".exe", ".msi"],
    "Code": [".py", ".java", ".cpp", ".c", ".html", ".css", ".js"]
}


def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():

        if extension.lower() in extensions:
            return category

    return "Others"


def organize_files(folder_path):

    if not os.path.exists(folder_path):
        print("❌ Folder does not exist.")
        return

    print("\n🔍 Scanning folder...\n")

    files_moved = 0

    for file_name in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file_name)

        # Ignore folders
        if os.path.isdir(file_path):
            continue

        # Get file extension
        _, extension = os.path.splitext(file_name)

        # Find category
        category = get_category(extension)

        # Create category folder
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok=True)

        # Destination path
        destination = os.path.join(category_folder, file_name)

        # Move file
        try:
            shutil.move(file_path, destination)

            print(f"✅ {file_name} → {category}")

            files_moved += 1

        except Exception as error:
            print(f"❌ Error moving {file_name}: {error}")

    print("\n==============================")
    print("     ORGANIZATION COMPLETE")
    print("==============================")
    print(f"Files moved: {files_moved}")