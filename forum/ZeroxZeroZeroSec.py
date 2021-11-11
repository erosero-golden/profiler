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


class ZeroxZeroZeroSec:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['0x00sec']['rate_limit'] / 1000
        # https://0x00sec.org/u/{username}
        self.format = config['plateform']['0x00sec']['format']
        # 0x00sec.org usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # forum
        self.type = config['plateform']['0x00sec']['type']

    # Generate all potential 0x00sec usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        zeroxzerozerosec_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
                # If the account exists
                if r.status_code == 200:
                    zeroxzerozerosec_usernames["accounts"].append({"value": username})
            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a 0x00sec.org')

            time.sleep(self.delay)

        return zeroxzerozerosec_usernames
