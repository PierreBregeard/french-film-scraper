from .Result import Result
from ..Selectable import Selectable

class SearchResult(Result):

    def __init__(self, url: str, title: str, year: str, director: str):
        super().__init__()
        self.url = url
        self.title = title
        self.year = year
        self.director = director

    def get_selectable(self):
        return Selectable(
            self.url,
            [self.title, f"{self.year} {self.director}"]
        )
