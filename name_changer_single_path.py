import os

def rename_folders_sequential(path):
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    folders.sort()

    temp_paths = []
    for idx, folder in enumerate(folders):
        old_path = os.path.join(path, folder)
        temp_path = os.path.join(path, f"__tmp__{idx}")
        os.rename(old_path, temp_path)
        temp_paths.append(temp_path)

    for i, temp_path in enumerate(temp_paths, start=1):
        new_path = os.path.join(path, str(i))
        os.rename(temp_path, new_path)
        print(f"{os.path.basename(temp_path)}  -->  {i}")

if __name__ == "__main__":
    rename_folders_sequential("DATASET_DIR_PATH")
