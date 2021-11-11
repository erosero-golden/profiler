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


class CrackedTo:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['crackedto']['rate_limit'] / 1000
        # https://cracked.to/{username}
        self.format = config['plateform']['crackedto']['format']
        # cracked.to usernames are not case sensitive
        self.permutationsList = permutationsList
        # forum
        self.type = config['plateform']['crackedto']['type']

    # Generate all potential cracked.to usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        cracked_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to cracked.to")

            # If the account exists
            if r.status_code == 200:
                cracked_usernames["accounts"].append({"value": username})
            time.sleep(self.delay)

        return cracked_usernames
