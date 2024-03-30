import webbrowser
import sys
from os import get_terminal_size
from textwrap import wrap
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from termcolor import cprint
from halo import Halo

from .Entity.Selectable import Selectable
from .FilmScraperController import FilmScraperController

class FilmScraperVue:

    def __init__(self):
        self.spinner = Halo(text="Recherche", spinner="dots")

        with self.spinner:
            self.fs = FilmScraperController()

    def center_text(self, text: str):
        """Print the text in the center of the screen with a padding."""
        padding = 1/10
        terminal_width = get_terminal_size().columns
        available_width = int((1 - padding * 2) * terminal_width)
        text_lines = wrap(text, available_width)

        for line in text_lines:
            left_padding = (terminal_width - len(line)) // 2
            print(f"{' ' * left_padding}{line}")

    def print_seperator(self):
        """Print a separtor made of '-' all across the screen."""
        print(get_terminal_size().columns * "-")

    def clear_upper_line(self, nb_lines: int = 1):
        """Clear nb_lines in the terminal"""
        for _ in range(nb_lines):
            print(f"\033[A{get_terminal_size().columns * ' '}\033[A")

    def print_disclaimer(self):
        """Print app disclaimer."""
        self.print_seperator()
        self.center_text("Conformément à la législation française, le téléchargement d'un fichier est autorisé uniquement si vous possédez l'original du film convoité. Il est important de noter que ni le présent logiciel, ni les hébergeurs, ni aucune autre partie ne sauraient être tenus pour responsables d'une utilisation inappropriée ou illégale de ce logiciel.")
        print()
        self.center_text("© 2024 - πR")
        self.print_seperator()

    def select_item(
        self,
        choices: list[Choice],
        message: str,
        additional_choices: list[Choice] | None = None) -> str:
        """Prompt the user to choose from choices given in params."""

        def format_res(res: str):
            # remove long spaces
            res = " ".join(res.split())
            return res.replace("(recommandé)", "")

        choices_formated: list[Choice|Separator]= []
        choices_formated += choices
        if additional_choices is not None:
            choices_formated += [
                Separator(),
                *additional_choices
            ]

        key = inquirer.select(
            pointer=">",
            message=message,
            choices=choices_formated,
            transformer=format_res,
            border=True
        ).execute()

        return key

    def ask_question(self, q: str):
        """Ask a question to the user in the terminal."""
        return inquirer.text(message=q).execute()

    def select_film(self) -> str:
        """Ask user to select a film after asking a prompt and return the film url's."""
        search_depth = 2
        search_prompt = self.ask_question("Entrer le nom du film :")

        while True:

            with self.spinner:
                film_selectables = self.fs.get_films(search_prompt, search_depth)
                film_choices = Selectable.parse_choices(film_selectables)

                additionnal_choices = [
                    Choice(name="Nouvelle recherche", value="search"),
                    Choice(name="Quitter", value= "exit")
                ]
                if search_depth < 5:
                    additionnal_choices.insert(0,
                        Choice(name="Recherche approfondie", value="more")
                    )

            menu_res = self.select_item(
                film_choices,
                "Sélectionner votre film :",
                additionnal_choices
            )

            match menu_res:
                case "exit":
                    sys.exit(0)
                case "search":
                    self.clear_upper_line(nb_lines=2)
                    return self.select_film()
                case "more":
                    self.clear_upper_line()
                    search_depth += 3
                case _: # Normally a url
                    return menu_res

    def select_resolution(self, film_url: str):
        """Ask user to select a film resolution from a film url."""
        with self.spinner:
            film_res_selectables = self.fs.get_film_resolutions(film_url)
            film_res_choices = Selectable.parse_choices(film_res_selectables)
        return self.select_item(
            film_res_choices,
            "Sélectionner la qualité :"
        )

    def select_dl(self, film_url: str):
        """Ask user to select a host from a film url."""
        with self.spinner:
            film_dl_selectables = self.fs.get_film_dl(film_url)
            film_dl_choices = Selectable.parse_choices(film_dl_selectables)
        return self.select_item(
            film_dl_choices,
            "Sélectionner l'hébergeur :"
        )

    def run(self):
        """Run the program."""
        self.print_disclaimer()
        film_url = self.select_film()
        film_url = self.select_resolution(film_url)
        dl_url = self.select_dl(film_url)
        webbrowser.open(dl_url)
        print("\nRedirection sur :")
        cprint(dl_url, "light_blue", attrs=["underline"])
        input("\nAppuyez sur n'importe quelle touche pour arrêter le programme")
