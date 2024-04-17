from pathlib import Path

from abc import ABC, abstractmethod

class Env(ABC):

    @staticmethod
    @abstractmethod
    def is_prod_env():
        """Return true if script running in a prod env else false"""
        env_path = Path(".env")

        # if file doesn't exist return true
        if not env_path.exists():
            return True

        with open(".env", "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        for line in lines:
            if "APP_ENV=" in line:
                return line.split("=", 1)[1] == "prod"
        return False
