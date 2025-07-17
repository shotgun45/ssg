import os
import shutil
import sys
from generatepage import generate_pages_recursive

def copy_recursive(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        dest_dir = os.path.join(target, rel_path) if rel_path != '.' else target
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(dest_dir, file)
            shutil.copy2(source_file, target_file)
            print(f"Copied: {source_file} -> {target_file}")

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists("docs"):
        shutil.rmtree("docs")

    copy_recursive("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()