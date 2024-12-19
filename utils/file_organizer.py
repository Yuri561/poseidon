import os
import shutil

def organize_files(directory, categories, delete_empty_folders, dry_run, organize_by_date):
    if not os.path.exists(directory):
        return f"Directory {directory} does not exist."

    log = []
    for folder, extensions in categories.items():
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path) and not dry_run:
            os.makedirs(folder_path)

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and any(file_path.endswith(ext) for ext in extensions):
                if not dry_run:
                    shutil.move(file_path, folder_path)
                log.append(f"Moved {filename} to {folder}")

    return "\n".join(log)
