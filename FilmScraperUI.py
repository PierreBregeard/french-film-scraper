from FilmScraper import FilmScraper
from simple_term_menu import TerminalMenu
from requests.exceptions import ConnectionError
from os import get_terminal_size
import webbrowser

class FilmScraperUI:

    film_id = ""

    def __init__(self):
        try:
            self.fs = FilmScraper()
        except ConnectionError:
            print("Connection error: Unable to establish a connection to the server")
            exit(1)

        self.print_seperator()
        self.center_text("Under French law, you are authorized to download a file only if you possess the original copy of the desired film. Neither this software, nor the hosts, nor anyone else can be held responsible for misuse of this software.")
        self.center_text("© 2024 - πR")
        self.print_seperator()
        print()

    def center_text(self, text):
        terminal_width = get_terminal_size().columns
        if len(text) > terminal_width:
            lines = text.split()
            new_lines = []
            current_line = ""
            for word in lines:
                if len(current_line) + len(word) + 1 > terminal_width:
                    new_lines.append(current_line)
                    current_line = word + " "
                else:
                    current_line += word + " "
            new_lines.append(current_line.strip())

            for line in new_lines:
                padding = (terminal_width - len(line)) // 2
                print(" " * padding + line)
        else:
            padding = (terminal_width - len(text)) // 2
            print(" " * padding + text)

    def print_seperator(self):
        print(get_terminal_size().columns * "-")

    def replace_last_line(self, new_line = None):
        print(f"\033[A{get_terminal_size().columns * ' '}\033[A")
        if new_line:
            print(new_line)

    def select_item(self, map, additional_map = None):
        map_options = list(map.keys())
        map_options.sort(key=lambda o: not "recommended" in o.lower())
        if additional_map:
            if (len(map_options) != 0):
                map_options += [None]
            map_options += list(additional_map.keys())
            map = {**map, **additional_map}
        i = TerminalMenu(map_options).show()
        key = map_options[i]
        # remove spaces
        return " ".join(key.split()), map[key]
    
    def select_film(self):
        search_range = 2
        search_i = 0
        searchs_soup = []

        search_text_input = "search : "
        search = input(search_text_input)
        while True:
            search_urls = []
            while search_i < search_range:
                search_urls.append(self.fs.add_search_to_url(search, page_index=search_i))
                search_i += 1
            
            searchs_soup += self.fs.get_soups(search_urls)
            film_map = self.fs.get_film_map(searchs_soup)
            
            additionnal_map= {}
            if search_range < 5:
                additionnal_map["fetch more"] = "more"
            additionnal_map["new research"] = "search"
            additionnal_map["exit"] = "exit"
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
        return self.fs.get_soup(film_url)

    def select_resolution(self, film_soup):
        film_res_map = self.fs.get_film_resolutions_map(film_soup, self.film_id)
        film_res_text, film_res_id = self.select_item(film_res_map)
        print(film_res_text)

        if film_res_id != self.film_id:
            self.film_id = film_res_id
            film_url = self.fs.add_film_id_to_url(self.film_id)
            film_soup = self.fs.get_soup(film_url)
        
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
        print("Redirected to :")
        print(film_dl_link)
        input("\nPress any key to close the program")

if __name__ == "__main__":
    fsUI = FilmScraperUI()
    fsUI.show()