import os

from pathlib import Path
from datetime import datetime

if __name__ == "__main__":

    root_path = Path(__file__).parent
    os.chdir(root_path)

    is_windows = os.name == 'nt'

    name = 'film-scraper'
    if is_windows:
        name += '.exe'

    # https://github.com/upx/upx/releases/tag/v4.2.4
    command = f"python -m PyInstaller --noconfirm --clean --console --onefile --upx-dir upx --name {name} "
    command += "--icon fav.ico "
    command += f"--add-data '.env'{';' if is_windows else ':'}'.env' "
    command += "main.py"
    os.system(command)

    exe_folder = root_path / Path(f"dist/{name}")
    print(f"Built in {exe_folder}")

    with open("version.txt", "w", encoding="utf-8") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
