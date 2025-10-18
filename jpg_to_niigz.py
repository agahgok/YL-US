from pathlib import Path
import re
import numpy as np
import imageio.v3 as iio
import SimpleITK as sitk

FRAMES_DIR = Path(r"file path")
OUT_NII    = Path(r"file path")
PAD_MODE   = "constant"

def natural_sort_key(p: Path):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', p.stem)]

files = sorted(
    [*FRAMES_DIR.glob("*.jpg"), *FRAMES_DIR.glob("*.jpeg"), *FRAMES_DIR.glob("*.JPG"), *FRAMES_DIR.glob("*.JPEG")],
    key=natural_sort_key
)
if not files:
    raise FileNotFoundError(f"No JPG files found in: {FRAMES_DIR}")

imgs = []
Hmax = Wmax = 0
for f in files:
    a = iio.imread(str(f))
    if a.ndim == 3:
        a = (0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]).astype(np.uint8)
    else:
        a = a.astype(np.uint8)
    H, W = a.shape
    Hmax = max(Hmax, H); Wmax = max(Wmax, W)
    imgs.append(a)

stack = []
for a in imgs:
    H, W = a.shape
    pad_h = Hmax - H
    pad_w = Wmax - W
    if pad_h or pad_w:
        if PAD_MODE == "constant":
            a = np.pad(a, ((0, pad_h), (0, pad_w)), mode="constant", constant_values=0)
        else:
            a = np.pad(a, ((0, pad_h), (0, pad_w)), mode="edge")
    stack.append(a)

vol = np.stack(stack, axis=0).astype(np.uint8)
img_sitk = sitk.GetImageFromArray(vol)
img_sitk.SetSpacing((1.0, 1.0, 1.0))
OUT_NII.parent.mkdir(parents=True, exist_ok=True)
sitk.WriteImage(img_sitk, str(OUT_NII))

print(f"Total frames: {len(files)} | Target HxW: {Hmax}x{Wmax}")
print(f"NIfTI saved to: {OUT_NII}")
