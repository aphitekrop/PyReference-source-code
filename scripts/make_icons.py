#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

SRC = Path("icon_source.jpg")
OUT = Path("assets/icons")


def main():
    if not SRC.exists():
        print("Положи фото 1:1 в корень проекта под именем icon_source.jpg")
        return

    OUT.mkdir(parents=True, exist_ok=True)

    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    s = min(w, h)
    img = img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))

    for size in [48, 72, 96, 144, 180, 192, 512, 1024]:
        img.resize((size, size), Image.LANCZOS).save(OUT / f"icon-{size}.png", "PNG")

    # Баннер 1024x500 для Google Play (feature graphic)
    big = img.resize((1024, 1024), Image.LANCZOS)
    big.crop((0, 262, 1024, 762)).save(OUT / "feature-1024x500.png", "PNG")

    print("Иконки готовы в assets/icons/")


if __name__ == "__main__":
    main()