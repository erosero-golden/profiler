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


class AboutMe:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['aboutme']['rate_limit'] / 1000
        # https://about.me/{username}
        self.format = config['plateform']['aboutme']['format']
        self.permutationsList = permutationsList
        # entertainment
        self.type = config['plateform']['aboutme']['type']

    # Generate all potential aboutme usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        aboutme_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to aboutme")

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
                    user_username = str(soup.find_all(class_="name")[0].get_text()).strip() if soup.find_all(
                        class_="name") else None
                    user_location = str(soup.find_all(class_="location")[1].get_text()).strip() if soup.find_all(
                        class_="location") else None
                    user_role = str(soup.find_all(class_="role")[0].get_text()).strip() if soup.find_all(
                        class_="role") else None
                    user_description = str(soup.find_all(class_="short-bio")[0].get_text()).strip() if soup.find_all(
                        class_="short-bio") else None

                    account["username"] = {"name": "Username", "value": user_username}
                    account["location"] = {"name": "Location", "value": user_location}
                    account["role"] = {"name": "Role", "value": user_role}
                    account["description"] = {"name": "Description", "value": user_description}
                except:
                    pass

                # Append the account to the accounts table
                aboutme_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return aboutme_usernames
