from PIL import Image
from pathlib import Path

INPUT_DIR  = Path(r"file path")
OUTPUT_DIR = Path(r"file path")

VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

def ensure_rgb(img: Image.Image) -> Image.Image:
    """
    Convert the image to RGB on a black background.
    Properly handles modes like RGBA, LA, and P.
    """
    if img.mode == "RGB":
        return img
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, (0, 0, 0))
        bg.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[-1])
        return bg
    return img.convert("RGB")

def pad_to_square_black(img: Image.Image) -> Image.Image:

    w, h = img.size
    size = max(w, h)
    canvas = Image.new("RGB", (size, size), (0, 0, 0))
    left = (size - w) // 2
    top  = (size - h) // 2
    canvas.paste(img, (left, top))
    return canvas

def process_folder(input_dir: Path, output_dir: Path):
    if not input_dir.exists():
        print(f"Input folder not found: {input_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    files = [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTS]
    if not files:
        print("No processable images found.")
        return

    ok, failed = 0, 0
    for src in files:
        try:
            with Image.open(src) as im:
                im.load()
                im_rgb = ensure_rgb(im)
                out_img = pad_to_square_black(im_rgb)

                exif = im.info.get("exif")

                dst = output_dir / src.name
                save_params = {}
                if dst.suffix.lower() in (".jpg", ".jpeg"):
                    save_params.update(dict(quality=95, subsampling=0, optimize=True))
                    if exif:
                        save_params["exif"] = exif

                out_img.save(dst, **save_params)
                ok += 1
                print(f"Processed {src.name} -> {dst.name}")
        except Exception as e:
            failed += 1
            print(f"Skipped {src.name}: {e}")

    print(f"\nDone. Succeeded: {ok}, Skipped: {failed}")
    print(f"Outputs: {output_dir}")

if __name__ == "__main__":
    process_folder(INPUT_DIR, OUTPUT_DIR)
