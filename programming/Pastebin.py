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


class Pastebin:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['pastebin']['rate_limit'] / 1000
        # https://pastebin.com/u/{username}
        self.format = config['plateform']['pastebin']['format']
        self.permutationsList = permutationsList
        # programming
        self.type = config['plateform']['pastebin']['type']

    # Generate all potential pastebin usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        pastebin_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to pastebin")

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
                    user_profile_views = str(soup.find_all(class_='views')[0].get_text())
                    user_pastes_views = str(soup.find_all(class_='views')[1].get_text())
                    user_profile_creation_date = str(soup.find_all(class_='date-text')[0].get_text())

                    account["profile_views"] = {"name": "Profile Views", "value": user_profile_views}
                    account["pastes_views"] = {"name": "Pastes Views", "value": user_pastes_views}
                    account["profile_creation_date"] = {"name": "Creation Date", "value": user_profile_creation_date}
                except:
                    pass

                # Scrape the user pastes
                try:
                    user_pastes = []

                    pastes = soup.find_all(class_='maintable')[0].find_all('tr')

                    for paste in pastes[1:]:
                        columns = paste.find_all('td')
                        user_pastes.append({
                            "name": str(columns[0].get_text().strip()),
                            "added": str(columns[1].get_text().strip()),
                            "expires": str(columns[2].get_text().strip()),
                            "hits": str(columns[3].get_text().strip()),
                            "syntax": str(columns[4].get_text().strip())
                        })

                    account["user_pastes"] = {"name": "Pastes", "value": user_pastes}
                except:
                    pass

                # Append the account to the accounts table
                pastebin_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return pastebin_usernames
