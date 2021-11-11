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


class DailyMotion:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['dailymotion']['rate_limit'] / 1000
        # https://dailymotion.com/{username}
        self.format = config['plateform']['dailymotion']['format']
        self.permutationsList = permutationsList
        # entertainment
        self.type = config['plateform']['dailymotion']['type']

    # Generate all potential dailymotion usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        dailymotion_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to dailymotion")

            # If the account exists
            if r.status_code == 200:
                dailymotion_usernames["accounts"].append({"value": username})
            time.sleep(self.delay)

        return dailymotion_usernames
