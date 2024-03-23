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
        film_arr = []
        max_film_text_length = 0

        for search_soup in searchs_soup :
            for film_block in search_soup.select(".wa-sub-block"):

                title = film_block.select_one(".wa-sub-block-title > a")
                # removing langage in the title
                title_text = title.get_text().split("[", 1)[0].strip()

                max_film_text_length = max(len(title_text), max_film_text_length)
                
                description_block = film_block.select_one("div:nth-child(2) > div:nth-child(2) > div:nth-child(4) > ul:nth-child(1)")
                year = description_block.select_one("li:nth-child(4) > b:nth-child(2) > a:nth-child(1)").get_text()
                real = description_block.select_one("li:nth-child(2) > b:nth-child(2) > a:nth-child(1)").get_text()

                film_arr.append({
                    "title": title_text,
                    "desc" : f"{year} {real}",
                    "id"   : title["href"]
                })


        film_map = {}
        for film in film_arr:
            # if not in the map
            if not film_map.get(title_text):
                name = film["title"].ljust(max_film_text_length, " ")
                name += " - " + film["desc"]
                film_map[name] = film["id"]
            
        return film_map

    def get_film_resolutions_map(self, film_soup, current_film_id):

        max_res_length = [0] # using a array to be modified in f below

        def split_lang(restxt):
            res, lang = restxt.split("(", 1)
            res.strip()
            max_res_length[0] = max(len(res), max_res_length[0])
            return res, lang.replace("(", "").replace(")", "").strip()


        def format_resolution(res):
            res = res.replace("[", "").replace("]", "")
            res_split = res.rsplit("-", 1)
            if len(res_split) == 2:
                res = f"{res_split[0].strip()} ({res_split[1].strip()})"
            return res

        current_res = film_soup.select_one("div.wa-sub-block:nth-child(3) > div:nth-child(1) > i:nth-child(2)").get_text()

        resolutions_arr = [{
            "restitle": split_lang(format_resolution(current_res)),
            "id"      : current_film_id
        }]

        ul = film_soup.select_one(".wa-post-list-ofLinks")
        for anchor in ul.select("li > a"):
            res = anchor.get_text()
            resolutions_arr.append({
                "restitle": split_lang(res),
                "id"      : anchor["href"]
            })

        resolutions_map = {}
        for resolution in resolutions_arr:
            res, lang = resolution["restitle"]
            name = res.ljust(max_res_length[0] + 1, " ")
            name += "- " + lang
            if "HDLIGHT 1080p" in name:
                name += " (recommended)"
            resolutions_map[name] = resolution["id"]

        return resolutions_map
    
    def get_film_dl_map(self, film_soup):

        film_downloads_arr = []
        max_length_name = 0

        for tr in film_soup.select("#DDLLinks > tbody:nth-child(1) > tr"):
            name = tr.select_one("td:nth-child(2)").get_text()
            if name == "Anonyme":
                continue
            max_length_name = max(max_length_name, len(name))

            film_downloads_arr.append({
                "name": name,
                "size": tr.select_one("td:nth-child(3)").get_text(),
                "href": tr.select_one("a")["href"]
            })

        film_downloads_map = {}

        for film_dl in film_downloads_arr:
            name = film_dl["name"].ljust(max_length_name, " ")
            name += f" - {film_dl['size']}"
            if "1fichier" in name:
                name += " (recommended)"
            film_downloads_map[name] = film_dl["href"]

        return film_downloads_map
    
    def add_search_to_url(self, search, page_index = 1):

        def format_search(search):
            return search.strip().replace(" ", "+")

        return f"{self.wawa_url}/?p=films&search={format_search(search)}&page={page_index}"

    def add_film_id_to_url(self, film_id):
        return f"{self.wawa_url}/{film_id}"