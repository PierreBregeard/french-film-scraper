from .Result import Result
from ..Selectable import Selectable

class DownloadResult(Result):

    def __init__(self, url: str, host_name: str, file_size: str, recommanded: bool):
        super().__init__()
        self.url = url
        self.host_name = host_name
        self.file_size = file_size
        self.recommanded = recommanded

    def get_selectable(self):
        return Selectable(
            self.url,
            [self.host_name, self.file_size],
            self.recommanded
        )
