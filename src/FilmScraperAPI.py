import requests
from bs4 import BeautifulSoup

from .Entity.Result.DownloadResult import DownloadResult
from .Entity.Result.ResolutionResult import ResolutionResult
from .Entity.Result.SearchResult import SearchResult

class FilmScraperApi:

    resolutions_recommanded = ["HDLIGHT 1080p"]
    hosts_recommanded = ["1fichier", "Uptobox"]

    film_search_history: dict[str, SearchResult] = {}

    def __init__(self):
        self.wawa_url = self.__get_wawacity_url()

    def __get_url_from_film_id(self, film_id: str):
        """Get the url of the film with the id."""
        return f"{self.wawa_url}/{film_id}"

    def __get_soup(self, url: str):
        """Parse URL into BeautifulSoup obj."""
        default_timeout = 4 # seconds
        res = requests.get(url, timeout=default_timeout)

        if res.status_code != 200:
            raise ConnectionError()

        return BeautifulSoup(res.text, 'lxml')

    def __get_wawacity_url(self):
        """Retrieve wawacity url."""
        soup = self.__get_soup("https://t.me/s/Wawacity_officiel")
        title = soup.select_one(".tgme_header_title > span:nth-child(1)")
        assert title is not None
        extension = title.get_text().split(".", 1)[-1]
        return f"https://www.wawacity.{extension}"

    def add_search_to_url(self, search: str, page_index: int = 1):
        """Format the seach into the url."""

        def format_search(search: str):
            return search.strip().replace(" ", "+")

        return f"{self.wawa_url}/?p=films&search={format_search(search)}&page={page_index}"

    def get_films_list(self, search_urls: list[str]):
        """Get film list with urls."""
        duplicates: list[str] = []

        for search_url in search_urls:

            search_result = self.film_search_history.get(search_url)
            if search_result is not None:
                yield search_result
                continue

            search_soup = self.__get_soup(search_url)

            for film_block in search_soup.select(".wa-sub-block"):

                title = film_block.select_one(".wa-sub-block-title > a")
                assert title is not None
                # remove language in the title
                title_str = title.get_text().split("[", 1)[0].strip()

                if not title_str in duplicates:
                    duplicates.append(title_str)
                else:
                    continue

                description_block = film_block.select_one(
                    "div:nth-child(2) > div:nth-child(2) > div:nth-child(4) > ul:nth-child(1)"
                )
                assert description_block is not None
                year = description_block.select_one(
                    "li:nth-child(4) > b:nth-child(2) > a:nth-child(1)"
                )
                director = description_block.select_one(
                    "li:nth-child(2) > b:nth-child(2) > a:nth-child(1)"
                )
                assert year is not None and director is not None

                search_result = SearchResult(
                    self.__get_url_from_film_id(str(title["href"])),
                    title_str,
                    year.get_text(),
                    director.get_text()
                )

                self.film_search_history[search_url] = search_result
                yield search_result

    def get_film_resolutions(self, film_page_url: str):
        """Get available resolutions from a film page url."""

        def split_lang(restxt: str):
            res, lang = restxt.split("(", 1)
            return res.strip(), lang.replace("(", "").replace(")", "").strip()

        def format_resolution(restxt: str):
            restxt = restxt.replace("[", "").replace("]", "")
            res_split = restxt.rsplit("-", 1)
            if len(res_split) == 2:
                restxt = f"{res_split[0].strip()} ({res_split[1].strip()})"
            return restxt

        def is_recommanded(resolution: str):
            return resolution in self.resolutions_recommanded

        film_soup = self.__get_soup(film_page_url)

        current_res = film_soup.select_one(
            "div.wa-sub-block:nth-child(3) > div:nth-child(1) > i:nth-child(2)"
        )
        assert current_res is not None

        res, lang = split_lang(format_resolution(current_res.get_text()))

        yield ResolutionResult(
            film_page_url,
            res,
            lang,
            is_recommanded(res)
        )

        ul = film_soup.select_one(".wa-post-list-ofLinks")
        assert ul is not None
        for anchor in ul.select("li > a"):
            restxt = anchor.get_text()
            res, lang = split_lang(restxt)
            yield ResolutionResult(
                self.__get_url_from_film_id(str(anchor["href"])),
                res,
                lang,
                is_recommanded(res)
            )

    def get_film_dl(self, film_page_url: str):
        """Get the available downloads from a film page url."""

        def is_recommanded(host_name: str):
            return host_name in self.hosts_recommanded

        film_soup = self.__get_soup(film_page_url)
        for tr in film_soup.select("#DDLLinks > tbody:nth-child(1) > tr"):
            dl_name = tr.select_one("td:nth-child(2)")
            assert dl_name is not None
            dl_name_str = dl_name.get_text()
            if "Anonyme" in dl_name_str:
                continue
            size = tr.select_one("td:nth-child(3)")
            anchor = tr.select_one("a")
            assert size is not None and anchor is not None

            yield DownloadResult(
                str(anchor["href"]),
                dl_name_str,
                size.get_text(),
                is_recommanded(dl_name_str)
            )
