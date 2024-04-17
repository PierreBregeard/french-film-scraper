from pathlib import Path
import os
from shutil import rmtree

# git filter-branch -f --tree-filter "rm -rf dist" HEAD

if __name__ == "__main__":

    NAME = "film-scraper"

    root_path = Path(__file__).parent
    os.chdir(root_path)

    # https://github.com/upx/upx/releases/tag/v4.2.3
    UPX_DIR_PATH = "UPX"
    os.system(
        f"python3 -m PyInstaller --noconfirm --icon fav.ico --clean --console --onefile --upx-dir {UPX_DIR_PATH} --name {NAME} main.py"
    )
    exe_folder = root_path / Path(f"dist/{NAME}.exe")
    print(f"Built in {exe_folder}")

    rmtree("build", ignore_errors=True)
    if os.path.isfile("film-scraper.spec"):
        os.remove("film-scraper.spec")
