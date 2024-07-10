import os
from abc import ABC
from pathlib import Path
from base64 import b64encode
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

class API(ABC):

    def __init__(self):
        env_path = Path(".env.local" if Path(".env.local").is_file() else ".env")
        load_dotenv(env_path, override=True)
        self.cache_responses = os.getenv("APP_ENV") == "dev"

    def get_soup(self, url: str):
        """Parse URL into BeautifulSoup obj."""
        tmp_folder = Path("tmp/")
        tmp_file = tmp_folder / Path(b64encode(url.encode()).decode() + ".html")
        if self.cache_responses:
            tmp_folder.mkdir(parents=True, exist_ok=True)
            if tmp_file.is_file():
                with open(tmp_file, "r", encoding="utf-8") as f:
                    return BeautifulSoup(f.read(), "lxml")

        default_timeout = 4 # seconds
        res = requests.get(url, timeout=default_timeout)

        if res.status_code != 200:
            raise ConnectionError()

        if self.cache_responses:
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(res.text)

        return BeautifulSoup(res.text, "lxml")
