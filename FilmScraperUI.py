import webbrowser
from requests.exceptions import ConnectionError
from os import get_terminal_size
from textwrap import wrap
from halo import Halo
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from termcolor import cprint

from FilmScraper import FilmScraper

class FilmScraperUI:

    film_id = ""

    def __init__(self):

        self.spinner = [Halo(spinner="dots"), False]

        try:
            self.fs = FilmScraper()
        except ConnectionError:
            print("Erreur de connexion : impossible d'établir une connexion au serveur")
            exit(1)

        self.print_seperator()
        print()
        self.center_text("Conformément à la législation française, le téléchargement d'un fichier est autorisé uniquement si vous possédez l'original du film convoité. Il est important de noter que ni le présent logiciel, ni les hébergeurs, ni aucune autre partie ne sauraient être tenus pour responsables d'une utilisation inappropriée ou illégale de ce logiciel.")
        print()
        self.center_text("© 2024 - πR")
        print()
        self.print_seperator()
        print()

    def center_text(self, text):
        padding = 1/10
        terminal_width = get_terminal_size().columns
        available_width = int((1 - padding * 2) * terminal_width)
        text_lines = wrap(text, available_width)

        for line in text_lines:
            left_padding = (terminal_width - len(line)) // 2
            print(f"{' ' * left_padding}{line}")

    def print_seperator(self):
        print(get_terminal_size().columns * "-")

    def clear_upper_line(self, nb_lines = 1):
        print(f"\033[A{get_terminal_size().columns * ' '}\033[A")
        if nb_lines == 1:
            return
        return self.clear_upper_line(nb_lines - 1)

    def toogle_spinner(self):
        if self.spinner[1]:
            self.spinner[0].stop()
        else:
            self.spinner[0].start()
        self.spinner[1] = not self.spinner[1]

    def ask_question(self, q):
        return inquirer.text(message=q).execute()

    def format_map(self, map):
        values = list(map.values())
        if len(values) == 0:
            return None
        titles = [v["title"][0] for v in values]
        max_length = len(max(titles, key=len))
        new_map = {}
        for key, val in map.items():
            name = val["title"][0].ljust(max_length, " ")
            name += " - " + val["title"][1]
            if val.get("isRecommanded"):
                name += " (recommandé)"
            new_map[key] = name
        return new_map

    def select_item(self, map, message, additional_map = None):

        def format_res(res):
            # remove long spaces
            res = " ".join(res.split())
            return res.replace("(recommandé)", "")

        formatted_map = self.format_map(map)
        choices = []
        if formatted_map:
            choices = [Choice(value=k, name=v) for k, v in formatted_map.items()]
            choices = sorted(choices, key=lambda choice: not "(recommandé)" in choice.name.lower())
        if additional_map:
            choices += [
                Separator(),
                *[Choice(v, k) for k, v in additional_map.items()] 
                ]
        key = inquirer.select(
            message=message,
            choices=choices,
            transformer=format_res
        ).execute()

        return key
    
    def select_film(self):
        search_range = 2
        search_i = 0
        searchs_soup = []

        search = self.ask_question("Entrer le nom du film :")
        while True:
            search_urls = []
            while search_i < search_range:
                search_urls.append(self.fs.add_search_to_url(search, page_index=search_i))
                search_i += 1
            
            self.toogle_spinner()
            searchs_soup += self.fs.get_soups(search_urls)
            self.toogle_spinner()
            film_map = self.fs.get_film_map(searchs_soup)
            
            additionnal_map= {}
            if search_range < 5:
                additionnal_map["Recherche approfondie"] = "more"
            additionnal_map["Nouvelle recherche"] = "search"
            additionnal_map["Quitter"] = "exit"
            menu_res = self.select_item(film_map, "Sélectionner votre film :", additionnal_map)

            if menu_res == "exit":
                exit(0)

            if menu_res == "search":
                self.clear_upper_line(nb_lines=2)
                return self.select_film()
            
            if menu_res != "more":
                self.film_id = menu_res
                break

            self.clear_upper_line()
            search_range += 3

        film_url = self.fs.add_film_id_to_url(self.film_id)

        self.toogle_spinner()
        film_soup = self.fs.get_soup(film_url)
        self.toogle_spinner()
        return film_soup

    def select_resolution(self, film_soup):
        film_res_map = self.fs.get_film_resolutions_map(film_soup, self.film_id)
        film_res_id = self.select_item(film_res_map, "Sélectionner la qualité :")

        if film_res_id != self.film_id:
            self.film_id = film_res_id
            film_url = self.fs.add_film_id_to_url(self.film_id)
            self.toogle_spinner()
            film_soup = self.fs.get_soup(film_url)
            self.toogle_spinner()
        
        return film_soup

    def select_dl(self, film_soup):
        film_dl_map = self.fs.get_film_dl_map(film_soup)
        film_dl_link  = self.select_item(film_dl_map, "Sélectionner l'hébergeur :")
        return film_dl_link

    def show(self):
        film_soup = self.select_film()
        film_soup = self.select_resolution(film_soup)
        film_dl_link = self.select_dl(film_soup)
        webbrowser.open(film_dl_link)
        print("\nRedirection sur :")
        cprint(film_dl_link, "light_blue", attrs=["underline"])
        input("\nAppuyez sur n'importe quelle touche pour arrêter le programme")

if __name__ == "__main__":
    fsUI = FilmScraperUI()
    fsUI.show()