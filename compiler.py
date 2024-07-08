from pathlib import Path
import os

if __name__ == "__main__":

    root_path = Path(__file__).parent
    os.chdir(root_path)

    is_windows = os.name == 'nt'

    name = 'film-scraper'
    if is_windows:
        name += '.exe'

    # https://github.com/upx/upx/releases/tag/v4.2.4
    command = f"python -m PyInstaller --noconfirm --icon fav.ico --clean --console --onefile --upx-dir upx --name {name} main.py"
    os.system(command)

    exe_folder = root_path / Path(f"dist/{name}")
    print(f"Built in {exe_folder}")
