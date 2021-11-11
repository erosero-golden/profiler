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


class Skype:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['skype']['rate_limit'] / 1000
        # https://www.skypli.com/profile/{}
        self.format = config['plateform']['skype']['format']
        self.permutationsList = permutationsList
        # tchat
        self.type = config['plateform']['skype']['type']

    # Generate all potential skype usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        skype_usernames = {
            "type": self.type,
            "accounts": []
        }

        skypli_URL = "https://www.skypli.com/profile/{}"

        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                skypli_formatted_URL = skypli_URL.format(username)
                r = requests.get(skypli_formatted_URL)
                # If the account exists
                if r.status_code == 200:
                    skype_usernames["accounts"].append({"value": username})
            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a skype')

            time.sleep(self.delay)

        return skype_usernames
