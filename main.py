import sys

from src.FilmScraperVue import FilmScraperVue

if __name__ == "__main__":
    try:
        FilmScraperVue().run()
    except ConnectionError:
        print("Erreur de connexion : impossible d'établir une connexion au serveur.")
        sys.exit(1)
    except AssertionError:
        print("Erreur de vérification: un élément n'a pas été trouvé lors de l'interpolation d'une page.")
        sys.exit(1)
