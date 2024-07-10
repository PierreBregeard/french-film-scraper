import os

from .API import API

class VersionAPI(API):

    def get_latest_version(self):
        """Return the latest code version of the program."""
        version_url = os.getenv("APP_VERSION_URL")
        if version_url is None:
            return None
        try:
            soup = self.get_soup(version_url)
        except ConnectionError:
            return None
        if soup is None:
            return None
        return soup.get_text()
