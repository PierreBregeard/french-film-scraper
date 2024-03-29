from abc import ABC, abstractmethod
from ..Selectable import Selectable

class Result(ABC):

    @abstractmethod
    def get_selectable(self) -> Selectable:
        """Return result selectable."""
