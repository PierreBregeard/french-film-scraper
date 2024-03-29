from .Result import Result
from ..Selectable import Selectable

class ResolutionResult(Result):

    def __init__(self, url: str, resolution: str, language: str, recommanded: bool):
        super().__init__()
        self.url = url
        self.resolution = resolution
        self.language = language
        self.recommanded = recommanded

    def get_selectable(self):
        return Selectable(
            self.url,
            [self.resolution, self.language],
            self.recommanded
        )
