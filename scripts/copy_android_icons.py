#!/usr/bin/env python3
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "assets" / "icons"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

MAP = {
    48: "mipmap-mdpi",
    72: "mipmap-hdpi",
    96: "mipmap-xhdpi",
    144: "mipmap-xxhdpi",
    192: "mipmap-xxxhdpi",
}


def main():
    # Удаляем адаптивную иконку, чтобы Android использовал наши PNG
    anydpi = RES / "mipmap-anydpi-v26"
    if anydpi.exists():
        shutil.rmtree(anydpi)
        print("removed mipmap-anydpi-v26")

    for size, folder in MAP.items():
        dst = RES / folder
        dst.mkdir(parents=True, exist_ok=True)
        src = ICONS / f"icon-{size}.png"
        if src.exists():
            shutil.copy(src, dst / "ic_launcher.png")
            shutil.copy(src, dst / "ic_launcher_round.png")
            print(f"{size} -> {folder}")

    print("Android icons copied")


if __name__ == "__main__":
    main()