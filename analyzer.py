import os


def analyze_folder(folder_path):
    """Analyze files inside a folder."""

    total_files = 0

    categories = {
        "Images": 0,
        "Documents": 0,
        "Videos": 0,
        "Music": 0,
        "Code": 0,
        "Others": 0
    }

    for root, folders, files in os.walk(folder_path):

        for file_name in files:

            total_files += 1

            extension = os.path.splitext(file_name)[1].lower()

            if extension in [".jpg", ".jpeg", ".png", ".gif"]:
                categories["Images"] += 1

            elif extension in [".pdf", ".doc", ".docx", ".txt"]:
                categories["Documents"] += 1

            elif extension in [".mp4", ".mkv", ".avi"]:
                categories["Videos"] += 1

            elif extension in [".mp3", ".wav"]:
                categories["Music"] += 1

            elif extension in [".py", ".java", ".cpp", ".c", ".html", ".css", ".js"]:
                categories["Code"] += 1

            else:
                categories["Others"] += 1

    return total_files, categories