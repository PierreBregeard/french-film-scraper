from pathlib import Path

from .Entity.Selectable import Selectable
from .API.FilmScraperAPI import FilmScraperApi
from .API.VersionAPI import VersionAPI

class FilmScraperController:

    def __init__(self):
        self.fk_api = FilmScraperApi()
        self.vs_api = VersionAPI()

    def __sort_selectables_by_recommanded(self, selectables: list[Selectable]):
        return sorted(selectables, key=lambda s: s.is_recommanded, reverse=True)


    def get_films(self, search: str, search_depth: int):
        """Get films selectables from search."""
        search_urls = [
            self.fk_api.add_search_to_url(search, i) for i in range(search_depth)
        ]
        films = self.fk_api.get_films_list(search_urls)
        return list(map(lambda f: f.get_selectable(), films))

    def get_film_resolutions(self, film_page_url: str):
        """Get resolutions selectables from a film page url."""
        film_resolutions = self.fk_api.get_film_resolutions(film_page_url)
        return self.__sort_selectables_by_recommanded(
            list(map(lambda f: f.get_selectable(), film_resolutions))
        )

    def get_film_dl(self, film_page_url: str):
        """Get downloads selectables from a film page url."""
        film_dl = self.fk_api.get_film_dl(film_page_url)
        return self.__sort_selectables_by_recommanded(
            list(map(lambda f: f.get_selectable(), film_dl))
        )

    def is_program_up_to_date(self):
        """Return True if the program version is the same as on the repo."""
        version_path = Path("version.txt")
        if not version_path.is_file():
            return False
        latest_version = self.vs_api.get_latest_version()
        if latest_version is None:
            return None
        current_version = version_path.read_text("utf-8")
        return current_version == latest_version
