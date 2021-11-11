__author__ = "Eduardo Tuteggito Rosero"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eduardo Tuteggito Rosero"
__email__ = "zerhiphop@live.com"
__status__ = "Development"
__date__ = "10/November/2021"

import requests
from bs4 import BeautifulSoup
import time

from tuteggito.enrich.basics.utils.Logger import Logger


class HackerNews:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['hackernews']['rate_limit'] / 1000
        # https://news.ycombinator.com/user?id={username}
        self.format = config['plateform']['hackernews']['format']
        # hackernews usernames are not case sensitive
        self.permutationsList = permutationsList
        # forum
        self.type = config['plateform']['hackernews']['type']

    # Generate all potential hackernews usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        hackernews_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to hackernews")

            # If the account exists
            if r.text.find("No such user.") != 0:
                # Account object
                account = {}

                # Get the username
                account["value"] = username

                # Parse HTML response content with beautiful soup 
                soup = BeautifulSoup(r.text, 'html.parser')

                # Scrape the user informations
                try:
                    user_creation_date = str(
                        soup.find_all("table")[2].find_all("td")[3].get_text()).strip() if soup.find_all(
                        "table") else None
                    user_karma = str(soup.find_all("table")[2].find_all("td")[5].get_text()).strip() if soup.find_all(
                        "table") else None

                    account["creation_date"] = {"name": "Creation Date", "value": user_creation_date}
                    account["karma"] = {"name": "Karma", "value": user_karma}
                except:
                    pass

                # Append the account to the accounts table
                hackernews_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return hackernews_usernames
