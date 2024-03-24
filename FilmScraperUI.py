from FilmScraper import FilmScraper
from requests.exceptions import ConnectionError
from os import get_terminal_size
from rich.console import Console
import webbrowser
from textwrap import wrap
from beaupy import select
from beaupy.spinners import Spinner, DOTS

class FilmScraperUI:

    film_id = ""

    def __init__(self):

        self.console = Console()

        try:
            self.fs = FilmScraper()
        except ConnectionError:
            print("Erreur de connexion : impossible d'établir une connexion au serveur")
            exit(1)

        self.print_seperator()
        self.center_text("Conformément à la législation française, le téléchargement d'un fichier est autorisé uniquement si vous possédez l'original du film convoité. Il est important de noter que ni le présent logiciel, ni les hébergeurs, ni aucune autre partie ne sauraient être tenus pour responsables d'une utilisation inappropriée ou illégale de ce logiciel.")
        print()
        self.center_text("© 2024 - πR")
        self.print_seperator()
        print()

    def center_text(self, text):
        padding = 1/8
        terminal_width = get_terminal_size().columns
        available_width = int((1 - padding * 2) * terminal_width)
        text_lines = wrap(text, available_width)

        for line in text_lines:
            left_padding = (terminal_width - len(line)) // 2
            print(f"{' ' * left_padding}{line}")

    def print_seperator(self):
        print(get_terminal_size().columns * "-")

    def replace_last_line(self, new_line = None):
        print(f"\033[A{get_terminal_size().columns * ' '}\033[A")
        if new_line:
            print(new_line)

    def select_item(self, map, additional_map = None):
        map_options = list(map.keys())
        map_options.sort(key=lambda o: not "recommandé" in o.lower())
        if additional_map:
            map_options += list(additional_map.keys())
            map = {**map, **additional_map}

        key = select(map_options, cursor=">", cursor_style="red")
        # remove spaces
        return " ".join(key.split()), map[key]
    
    def select_film(self):
        search_range = 2
        search_i = 0
        searchs_soup = []

        search_text_input = "film recherché : "
        search = input(search_text_input)
        while True:
            search_urls = []
            while search_i < search_range:
                search_urls.append(self.fs.add_search_to_url(search, page_index=search_i))
                search_i += 1
            
            spinner = Spinner(DOTS, "")
            spinner.start()
            searchs_soup += self.fs.get_soups(search_urls)
            spinner.stop()
            film_map = self.fs.get_film_map(searchs_soup)
            
            additionnal_map= {}
            if search_range < 5:
                additionnal_map["recherche approfondie"] = "more"
            additionnal_map["nouvelle recherche"] = "search"
            additionnal_map["quitter"] = "exit"
            menu_text, menu_res = self.select_item(film_map, additionnal_map)

            if menu_res == "exit":
                exit(0)
            if menu_res == "search":
                self.replace_last_line()
                return self.select_film()
            if menu_res != "more":
                self.film_id = menu_res
                self.replace_last_line(search_text_input + menu_text)
                break

            search_range += 3

        film_url = self.fs.add_film_id_to_url(self.film_id)

        spinner.start()
        film_soup = self.fs.get_soup(film_url)
        spinner.stop()
        return film_soup

    def select_resolution(self, film_soup):
        film_res_map = self.fs.get_film_resolutions_map(film_soup, self.film_id)
        film_res_text, film_res_id = self.select_item(film_res_map)
        print(film_res_text)

        if film_res_id != self.film_id:
            self.film_id = film_res_id
            film_url = self.fs.add_film_id_to_url(self.film_id)
            spinner = Spinner(DOTS, "")
            spinner.start()
            film_soup = self.fs.get_soup(film_url)
            spinner.stop()
        
        return film_soup

    def select_dl(self, film_soup):
        film_dl_map = self.fs.get_film_dl_map(film_soup)
        film_dl_text, film_dl_link  = self.select_item(film_dl_map)
        print(film_dl_text)
        return film_dl_link

    def show(self):
        film_soup = self.select_film()
        film_soup = self.select_resolution(film_soup)
        film_dl_link = self.select_dl(film_soup)
        webbrowser.open(film_dl_link)
        print("Redirection sur :")
        self.console.print(film_dl_link)
        input("\nAppuyez sur n'importe quelle touche pour arrêter le programme")

if __name__ == "__main__":
    fsUI = FilmScraperUI()
    fsUI.show()