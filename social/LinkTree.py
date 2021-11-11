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


class LinkTree:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['linktree']['rate_limit'] / 1000
        # https://linktr.ee/{username}
        self.format = config['plateform']['linktree']['format']
        # linktree usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # social
        self.type = config['plateform']['linktree']['type']

    # Generate all potential linktree usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        linktree_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to linktree")

            # If the account exists
            if r.status_code == 200:
                # Account object
                account = {}

                # Get the username
                account["value"] = username

                # Parse HTML response content with beautiful soup 
                soup = BeautifulSoup(r.text, 'html.parser')

                # Scrape the user links
                try:
                    user_services = []

                    services = soup.find_all("div", {"data-testid": "StyledContainer"})

                    for service in services[1:]:
                        user_services.append({
                            "service": str(service.get_text().strip()),
                            "link": str(service.find_all('a', href=True)[0]['href'].strip())
                        })

                    account["user_services"] = {"name": "Services", "value": user_services}
                except:
                    pass

                # Append the account to the accounts table
                linktree_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return linktree_usernames
