from FilmScraper import FilmScraper
from simple_term_menu import TerminalMenu
import webbrowser

class FilmScraperUI:

    film_id = ""

    def __init__(self):
        self.fs = FilmScraper()

    def select_item(self, map):
        map_options = list(map.keys())
        map_options.sort(key=lambda o: not "recommended" in o.lower())
        i = TerminalMenu(map_options).show()
        return map[map_options[i]]
    
    def select_film(self):
        search_range = 1
        search = input("search : ")

        while True:
            search_urls = [""] * search_range
            for i in range(search_range):
                search_urls[i] = self.fs.add_search_to_url(search, page_index=i)
            
            searchs_soup = self.fs.get_soups(search_urls)
            film_map = self.fs.get_film_map(searchs_soup)
            
            if search_range < 5:
                film_map["fetch more.."] = None
            self.film_id = self.select_item(film_map)
            if self.film_id:
                break
            search_range += 2

        film_url = self.fs.add_film_id_to_url(self.film_id)
        return self.fs.get_soup(film_url)

    def select_resolution(self, film_soup):
        film_res_map = self.fs.get_film_resolutions_map(film_soup, self.film_id)
        film_res_id = self.select_item(film_res_map)

        if film_res_id != self.film_id:
            self.film_id = film_res_id
            film_url = self.fs.add_film_id_to_url(self.film_id)
            film_soup = self.fs.get_soup(film_url)
        
        return film_soup

    def select_dl(self, film_soup):
        film_dl_map = self.fs.get_film_dl_map(film_soup)
        return self.select_item(film_dl_map)

    def show(self):
        film_soup = self.select_film()
        film_soup = self.select_resolution(film_soup)
        film_dl_link = self.select_dl(film_soup) 
        webbrowser.open(film_dl_link)
        print(film_dl_link)
    
if __name__ == "__main__":
    fsUI = FilmScraperUI()
    fsUI.show()