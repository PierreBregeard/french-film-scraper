from pathlib import Path
import os
from shutil import rmtree

if __name__ == "__main__":

    name = "film-scraper"

    root_path = Path(__file__).parent
    os.chdir(root_path)
    upx_dir_path = "UPX"
    os.system(
        f"python -m PyInstaller --noconfirm --icon fav.ico --clean --console --onefile --upx-dir {upx_dir_path} --name {name} main.py"
    )
    exe_folder = root_path / Path(f"dist/{name}.exe")
    print(f"Built in {exe_folder}")

    rmtree("build", ignore_errors=True)
    if os.path.isfile("film-scraper.spec"):
        os.remove("film-scraper.spec")