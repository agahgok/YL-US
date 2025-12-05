import os

BASE_DIR = "BASE_DIR_PATH"

def count_png_files(base_dir):
    total_png = 0

    for root, dirs, files in os.walk(base_dir):
        png_count = sum(1 for f in files if f.lower().endswith(".png"))
        if png_count > 0:
            print(f"{root} → {png_count} adet PNG")
        total_png += png_count

    print("\n--------------------------------------")
    print(f"Toplam PNG sayısı: {total_png}")
    print("--------------------------------------")

if __name__ == "__main__":
    count_png_files(BASE_DIR)
