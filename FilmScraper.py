from bs4 import BeautifulSoup
import requests

class FilmScraper:

    def __init__(self):
        self.wawa_url = self.__get_wawacity_url()

    def __get_wawacity_url(self):
        soup = self.get_soup("https://t.me/s/Wawacity_officiel")
        title = soup.select_one(".tgme_header_title > span:nth-child(1)").get_text()
        extension = title.split(".", 1)[-1]
        return f"https://www.wawacity.{extension}"

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'lxml')
    
    def get_soups(self, urls):
        for url in urls:
            yield self.get_soup(url)
    
    def get_film_map(self, searchs_soup):
        film_map = {}

        for search_soup in searchs_soup :
            for title in search_soup.select(".wa-sub-block-title a"):
                title_text = title.get_text().split("[", 1)[0].strip()
                if not film_map.get(title_text):
                    film_map[title_text] = title["href"]
            
        return film_map

    def get_film_resolutions_map(self, film_soup, current_film_id):

        def add_recommended(res):
            res = res.strip()
            if "HDLIGHT 1080p" in res:
                res += " (recommended)"
            return res

        def format_resolution(res):
            res = res.replace("[", "").replace("]", "")
            res_split = res.rsplit("-", 1)
            if len(res_split) == 2:
                res = f"{res_split[0].strip()} ({res_split[1].strip()})"
            return res

        current_res = film_soup.select_one("div.wa-sub-block:nth-child(3) > div:nth-child(1) > i:nth-child(2)").get_text()
        current_res = add_recommended(format_resolution(current_res))

        resolutions_map = {
            current_res: current_film_id
        }

        ul = film_soup.select_one(".wa-post-list-ofLinks")
        for anchor in ul.select("li > a"): # test this
            res = add_recommended(anchor.get_text())
            resolutions_map[res] = anchor["href"]

        return resolutions_map
    
    def get_film_dl_map(self, film_soup):

        film_downloads_map = {}

        for tr in film_soup.select("#DDLLinks > tbody:nth-child(1) > tr"):
            name = tr.select_one("td:nth-child(2)").get_text()
            if name == "Anonyme":
                continue
            if name == "1fichier":
                name += " (recommended)"
            film_downloads_map[name] = tr.select_one("a")["href"]

        return film_downloads_map
    
    def add_search_to_url(self, search, page_index = 1):

        def format_search(search):
            return search.strip().replace(" ", "+")

        return f"{self.wawa_url}/?p=films&search={format_search(search)}&page={page_index}"

    def add_film_id_to_url(self, film_id):
        return f"{self.wawa_url}/{film_id}"