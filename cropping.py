from pathlib import Path
from PIL import Image, ImageOps, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

INPUT_DIR  = Path(r"file path")
OUTPUT_DIR = Path(r"file path")

LEFT_RIGHT = 292
TOP = 70

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

def compute_crop_rect(w: int, h: int):
    left  = LEFT_RIGHT
    upper = TOP
    right = w - LEFT_RIGHT
    lower = h
    if right - left < 1 or lower - upper < 1:
        raise ValueError(f"Image too small: {w}x{h} (requires min width {2*LEFT_RIGHT+1}, height {TOP+1}).")
    return (left, upper, right, lower)

def main():
    if not INPUT_DIR.exists():
        print(f"Input folder not found: {INPUT_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = [p for p in INPUT_DIR.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    if not files:
        print(f"No suitable images found in {INPUT_DIR}.")
        return

    ok, skipped = 0, 0
    for src in sorted(files):
        try:
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im)
                w, h = im.size
                rect = compute_crop_rect(w, h)
                cropped = im.crop(rect)

                dst = OUTPUT_DIR / src.name

                ext = dst.suffix.lower()
                save_kwargs = {}

                if ext in {".jpg", ".jpeg"}:
                    save_kwargs.update(dict(quality=95, optimize=True))
                elif ext == ".png":
                    save_kwargs.update(dict(optimize=True, compress_level=6))

                cropped.save(dst, **save_kwargs)

                ok += 1
                print(f"{src.name}: {w}x{h} -> crop {rect} -> {dst.name}")

        except Exception as e:
            skipped += 1
            print(f"Skipped: {src.name} ({e})")

    print(f"\nDone. Succeeded: {ok}, Skipped: {skipped}")
    print(f"Outputs: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
