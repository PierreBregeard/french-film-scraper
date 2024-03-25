from bs4 import BeautifulSoup
import requests

class FilmScraper:

    recommended_text = " (recommandé)"

    def __init__(self):
        self.wawa_url = "https://www.wawacity.tokyo" # self.__get_wawacity_url()

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

    def is_recommended(self, type, text):
        if type == "res":
            recommandations = ["HDLIGHT 1080p"]
        elif type == "dl":
            recommandations = ["1fichier", "Uptobox"]
        else: return False

        for recommandation in recommandations:
            if text in recommandation:
                return True
        return False
    
    def get_film_map(self, searchs_soup):

        film_map = {}

        for search_soup in searchs_soup :
            for film_block in search_soup.select(".wa-sub-block"):

                title = film_block.select_one(".wa-sub-block-title > a")
                # removing langage in the title
                title_text = title.get_text().split("[", 1)[0].strip()
                
                description_block = film_block.select_one("div:nth-child(2) > div:nth-child(2) > div:nth-child(4) > ul:nth-child(1)")
                year = description_block.select_one("li:nth-child(4) > b:nth-child(2) > a:nth-child(1)").get_text()
                real = description_block.select_one("li:nth-child(2) > b:nth-child(2) > a:nth-child(1)").get_text()
                desc = f"{year} {real}"
                film_map[f"{title_text}|~|{desc}"] = title["href"]

        return film_map

    def get_film_resolutions_map(self, film_soup, current_film_id):

        def split_lang(restxt):
            res, lang = restxt.split("(", 1)
            return res.strip(), lang.replace("(", "").replace(")", "").strip()

        def format_resolution(res):
            res = res.replace("[", "").replace("]", "")
            res_split = res.rsplit("-", 1)
            if len(res_split) == 2:
                res = f"{res_split[0].strip()} ({res_split[1].strip()})"
            return res

        current_res = film_soup.select_one("div.wa-sub-block:nth-child(3) > div:nth-child(1) > i:nth-child(2)").get_text()

        resolutions_map = {}

        res, lang = split_lang(format_resolution(current_res))
        if self.is_recommended("res", res):
            lang += self.recommended_text
        resolutions_map[f"{res}|~|{lang}"] = current_film_id

        ul = film_soup.select_one(".wa-post-list-ofLinks")
        for anchor in ul.select("li > a"):
            restxt = anchor.get_text()
            res, lang = split_lang(restxt)
            if self.is_recommended("res", res):
                lang += self.recommended_text
            resolutions_map[f"{res}|~|{lang}"] = anchor["href"]

        return resolutions_map
    
    def get_film_dl_map(self, film_soup):

        film_downloads_map = {}

        for tr in film_soup.select("#DDLLinks > tbody:nth-child(1) > tr"):
            dl_name = tr.select_one("td:nth-child(2)").get_text()
            if dl_name == "Anonyme":
                continue

            size = tr.select_one("td:nth-child(3)").get_text()
            if self.is_recommended("dl", dl_name):
                size += self.recommended_text

            film_downloads_map[f"{dl_name}|~|{size}"] = tr.select_one("a")["href"]

        return film_downloads_map
    
    def add_search_to_url(self, search, page_index = 1):

        def format_search(search):
            return search.strip().replace(" ", "+")

        return f"{self.wawa_url}/?p=films&search={format_search(search)}&page={page_index}"

    def add_film_id_to_url(self, film_id):
        return f"{self.wawa_url}/{film_id}"