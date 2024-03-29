from InquirerPy.base.control import Choice

class Selectable:

    recommanded_str = "(recommandé)"
    title_splitter_str = " - "

    def __init__(self, url: str, title: list[str], is_recommanded: bool = False):
        self.url = url
        self.title = title
        self.is_recommanded = is_recommanded

    @staticmethod
    def parse_choices(selectables: list['Selectable']):
        """Parse the selectables into a inquirer choices correctly formated with spaces."""

        def get_max_length(arr: list[str]):
            """Return the length of the biggest string in the list."""
            return len(max(arr, key=len))

        # selectable.title is always a list with 2 elements
        max_length_first_title_part = get_max_length(
            list(map(lambda s: s.title[0], selectables))
        )

        def format_title(title: list[str], is_recommanded: bool):
            title_str = title[0].strip().ljust(max_length_first_title_part)
            title_str += Selectable.title_splitter_str + title[1].strip()
            if is_recommanded:
                title_str += f" {Selectable.recommanded_str}"
            return title_str

        return list(map(
            lambda s: Choice(value=s.url, name=format_title(s.title, s.is_recommanded)), selectables
        ))
