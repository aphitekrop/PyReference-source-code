#!/usr/bin/env python3
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WWW = ROOT / "www"

FILES = [
    "index.html",
    "entry.html",
    "articles.html",
    "article.html",
    "login.html",
    "manifest.webmanifest",
    "sw.js",
]

DIRS = ["assets", "data"]


def main():
    if WWW.exists():
        shutil.rmtree(WWW)
    WWW.mkdir(parents=True)

    for f in FILES:
        src = ROOT / f
        if src.exists():
            shutil.copy(src, WWW / f)
        else:
            print(f"[warn] НЕТ файла в корне: {f}")

    for d in DIRS:
        src = ROOT / d
        if src.exists():
            shutil.copytree(src, WWW / d)

    print(f"Папка www готова: {WWW}")


if __name__ == "__main__":
    main()