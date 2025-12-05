import os

def rename_files_inside_folders(path):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    for folder in folders:
        folder_path = os.path.join(path, folder)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        files.sort()

        temp_paths = []
        for idx, filename in enumerate(files):
            old_file = os.path.join(folder_path, filename)
            temp_file = os.path.join(folder_path, f"__tmp__{idx}")
            os.rename(old_file, temp_file)
            temp_paths.append((temp_file, filename))

        for i, (tmp_file, oldname) in enumerate(temp_paths, start=1):
            extension = os.path.splitext(oldname)[1]
            new_name = f"{i}{extension}"
            new_path = os.path.join(folder_path, new_name)
            os.rename(tmp_file, new_path)

        print(f"{folder} completed.")

rename_files_inside_folders("DATASET_DIR_PATH")
