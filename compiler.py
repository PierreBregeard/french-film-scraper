from pathlib import Path
import os
from shutil import rmtree

if __name__ == "__main__":

    name = "film-scraper"

    root_path = Path(__file__).parent
    os.chdir(root_path)
    os.system(
        f"pyinstaller --clean --onefile --name {name} main.py"
    )
    exe_folder = root_path / Path("dist/{name}.exe")
    print(f"Built in {exe_folder}")

    rmtree("build", ignore_errors=True)
    os.remove("film-scraper.spec")