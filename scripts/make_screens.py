#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

SRC = Path("screens_src")   # сюда положи исходные скриншоты
OUT = Path("screens")       # отсюда заберёшь готовые

MIN_SIDE = 320
MAX_SIDE = 3840


def fix(img):
    # 24-бит, без альфа-канала
    img = img.convert("RGB")
    w, h = img.size

    # соотношение не длиннее 2:1 (обрезаем длинную сторону)
    if h > w * 2:
        img = img.crop((0, 0, w, w * 2))
        w, h = img.size
    if w > h * 2:
        img = img.crop((0, 0, h * 2, h))
        w, h = img.size

    # стороны в диапазоне 320..3840
    scale = 1.0
    if max(w, h) > MAX_SIDE:
        scale = MAX_SIDE / max(w, h)
    if min(w, h) * scale < MIN_SIDE:
        scale = MIN_SIDE / min(w, h)
    if scale != 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    return img


def main():
    SRC.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)

    files = sorted(
        list(SRC.glob("*.png")) + list(SRC.glob("*.jpg")) + list(SRC.glob("*.jpeg"))
    )

    if not files:
        print("Положи исходные скриншоты в папку screens_src")
        return

    for f in files:
        img = fix(Image.open(f))
        out_path = OUT / (f.stem + ".jpg")
        img.save(out_path, "JPEG", quality=92)
        print(f"{f.name} -> {img.size[0]}x{img.size[1]}  ({out_path})")


if __name__ == "__main__":
    main()