
from pathlib import Path

def rename_all_to_lowercase(folder_path: str):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ Doc does not exist: {folder_path}")
        return

    count = 0
    for file in folder.glob("*"):
        lower_name = file.name.lower()
        lower_path = file.parent / lower_name
        if file.name != lower_name:
            print(f"🔁 Rename: {file.name} → {lower_name}")
            file.rename(lower_path)
            count += 1


if __name__ == "__main__":
    rename_all_to_lowercase("**")
