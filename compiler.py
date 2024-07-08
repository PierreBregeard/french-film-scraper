from pathlib import Path
import os
from shutil import rmtree

if __name__ == "__main__":

    root_path = Path(__file__).parent
    os.chdir(root_path)

    # https://github.com/upx/upx/releases/tag/v4.2.3
    # UPX_DIR_PATH = "UPX"
    # os.system(
    #     f"python3 -m PyInstaller --noconfirm --icon fav.ico --clean --console --onefile --upx-dir {UPX_DIR_PATH} --name {NAME} main.py"
    # )

    is_windows = os.name == 'nt'

    name = 'film-scraper'
    if is_windows:
        name += '.exe'

    command = f"python -m PyInstaller --noconfirm --icon fav.ico --clean --console --onefile --name {name} main.py"
    os.system(command)

    exe_folder = root_path / Path(f"dist/{name}")
    print(f"Built in {exe_folder}")

    rmtree("build", ignore_errors=True)
    if os.path.isfile("film-scraper.spec"):
        os.remove("film-scraper.spec")
