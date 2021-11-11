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


class MySpace:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['myspace']['rate_limit'] / 1000
        # https://myspace.com/{username}
        self.format = config['plateform']['myspace']['format']
        self.permutationsList = permutationsList
        # social
        self.type = config['plateform']['myspace']['type']

    # Generate all potential myspace usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        myspace_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)

                # If the account exists
                if r.status_code == 200:
                    # Account object
                    account = {}

                    # Get the username
                    account["value"] = username

                    # Parse HTML response content with beautiful soup
                    soup = BeautifulSoup(r.text, 'html.parser')

                    # Scrape the user informations
                    try:
                        user_following_count = str(
                            soup.find_all("div", {"id": "connectionsCount"})[0].find_all("span")[0].get_text().replace(
                                ",",
                                "")) if soup.find_all(
                            "div", {"id": "connectionsCount"}) else None
                        user_followers_count = str(
                            soup.find_all("div", {"id": "connectionsCount"})[0].find_all("span")[1].get_text().replace(
                                ",",
                                "")) if soup.find_all(
                            "div", {"id": "connectionsCount"}) else None

                        account["following_count"] = {"name": "Following", "value": user_following_count}
                        account["followers_count"] = {"name": "Followers", "value": user_followers_count}

                    except:
                        self.log.error(f'Error en la búsqueda de información de {username} en myspace')

                    # Append the account to the accounts table
                    myspace_usernames["accounts"].append(account)

            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a myspace')

            time.sleep(self.delay)

        return myspace_usernames
