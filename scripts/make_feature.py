#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path("icon_source.jpg")                 # твоё фото 1:1
OUT = Path("screens") / "feature-1024x500.jpg"

W, H = 1024, 500
BG = (15, 23, 42)                             # тёмный фон как в приложении
TITLE = "PyReference"
SUBTITLE = "Справочник по Python"

FONT_PATHS = [
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\segoeui.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size):
    for fp in FONT_PATHS:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()


def fit_font(draw, text, start_size, max_w):
    size = start_size
    font = load_font(size)
    while size > 16:
        w = draw.textbbox((0, 0), text, font=font)[2]
        if w <= max_w:
            break
        size -= 4
        font = load_font(size)
    return font


def main():
    OUT.parent.mkdir(exist_ok=True)

    # квадрат из фото
    img = Image.open(SRC).convert("RGB")
    w, h = img.size
    s = min(w, h)
    img = img.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))

    canvas = Image.new("RGB", (W, H), BG)

    # иконка слева
    icon_size = 320
    icon = img.resize((icon_size, icon_size), Image.LANCZOS)
    ix, iy = 100, (H - icon_size) // 2
    canvas.paste(icon, (ix, iy))

    # текст справа
    draw = ImageDraw.Draw(canvas)
    tx = ix + icon_size + 60
    max_w = W - tx - 40

    f1 = fit_font(draw, TITLE, 72, max_w)
    f2 = fit_font(draw, SUBTITLE, 36, max_w)

    draw.text((tx, 160), TITLE, font=f1, fill=(147, 197, 253))
    draw.text((tx, 260), SUBTITLE, font=f2, fill=(203, 213, 225))

    canvas.save(OUT, "JPEG", quality=92)
    print(f"Сохранено: {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()