#!/usr/bin/env python3
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent

ORDER = [
    "build_entries.py",    
    "enhance_entries.py",   
    "expand_entries.py",    
    "build_articles.py",    
    "expand2_entries.py",   
    "expand3_entries.py",
    "expand4_entries.py",  
]

def run(script_name):
    path = HERE / script_name

    if not path.exists():
        print(f"[skip] {script_name} не найден")
        return

    spec = importlib.util.spec_from_file_location(script_name[:-3], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
    print(f"[ok] {script_name}")


def main():
    for script_name in ORDER:
        run(script_name)

    print("\nГотово. База собрана полностью.")


if __name__ == "__main__":
    main()