import os
import subprocess

DATASET_DIR = "DATASET_DIR_PATH"
OUT_DIR     = "OUTPUT_DIR_PATH"

def is_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False

def extract_all_frames():
    folders = [d for d in os.listdir(DATASET_DIR)
               if os.path.isdir(os.path.join(DATASET_DIR, d))]

    folders_numeric = sorted([d for d in folders if is_int(d)], key=lambda x: int(x))
    folders_other   = sorted([d for d in folders if not is_int(d)])
    folders = folders_numeric + folders_other

    for folder in folders:
        in_folder_path = os.path.join(DATASET_DIR, folder)
        out_folder_base = os.path.join(OUT_DIR, folder)
        os.makedirs(out_folder_base, exist_ok=True)

        videos = [f for f in os.listdir(in_folder_path)
                  if os.path.isfile(os.path.join(in_folder_path, f))
                  and f.lower().endswith(".mp4")]

        def video_key(name):
            base, _ = os.path.splitext(name)
            return int(base) if base.isdigit() else base

        videos.sort(key=video_key)

        for video_name in videos:
            video_path = os.path.join(in_folder_path, video_name)
            base_name, _ = os.path.splitext(video_name)

            out_dir = os.path.join(out_folder_base, base_name)
            os.makedirs(out_dir, exist_ok=True)

            output_pattern = os.path.join(out_dir, "%06d.png")

            cmd = [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-vsync", "0",
                output_pattern
            ]

            print(f"\n[INFO] {video_path} --> {out_dir}")
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] ffmpeg error: {video_path}")
                print(e)

if __name__ == "__main__":
    extract_all_frames()
