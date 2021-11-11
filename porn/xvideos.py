__author__ = "Eduardo Tuteggito Rosero"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eduardo Tuteggito Rosero"
__email__ = "zerhiphop@live.com"
__status__ = "Development"
__date__ = "10/November/2021"

import requests
import time

class XVideos:

    def __init__(self, config, permutationsList):
        # 1000 ms
        self.delay = config['plateform']['xvideos']['rate_limit'] / 1000
        # https://www.xvideos.com/profiles/{username}
        self.format = config['plateform']['xvideos']['format']
        # xvideos usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # xvideos
        self.type = config['plateform']['xvideos']['type']

    # Generate all potential xvideos usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation = permutation,
            ))
        return possibleUsernames

    def search(self):
        xvideos_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to xvideos")
            
            # If the account exists
            if r.status_code == 200:
                xvideos_usernames["accounts"].append({"value": username})
            time.sleep(self.delay)
        
        return xvideos_usernames