__author__ = "Eduardo Tuteggito Rosero"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eduardo Tuteggito Rosero"
__email__ = "zerhiphop@live.com"
__status__ = "Development"
__date__ = "10/November/2021"

import requests
import time

from tuteggito.enrich.basics.utils.Logger import Logger


class Spotify:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['spotify']['rate_limit'] / 1000
        # https://open.spotify.com/user/{}
        self.format = config['plateform']['spotify']['format']
        # spotify usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # spotify
        self.type = config['plateform']['spotify']['type']

    # Generate all potential spotify usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        spotify_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
                # If the account exists
                if r.status_code == 200:
                    spotify_usernames["accounts"].append({"value": username})
            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a spotify')

            time.sleep(self.delay)

        return spotify_usernames
