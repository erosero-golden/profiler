__author__ = "Eduardo Tuteggito Rosero"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eduardo Tuteggito Rosero"
__email__ = "zerhiphop@live.com"
__status__ = "Development"
__date__ = "10/November/2021"

import requests
import time

class Redtube:

    def __init__(self, config, permutationsList):
        # 1000 ms
        self.delay = config['plateform']['redtube']['rate_limit'] / 1000
        # https://fr.redtube.com/users/{username}
        self.format = config['plateform']['redtube']['format']
        # redtube usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # porn
        self.type = config['plateform']['redtube']['type']

    # Generate all potential redtube usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation = permutation,
            ))
        return possibleUsernames

    def search(self):
        redtube_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to redtube")
            
            # If the account exists
            if r.status_code == 200:
                redtube_usernames["accounts"].append({"value": username})
            time.sleep(self.delay)
        
        return redtube_usernames