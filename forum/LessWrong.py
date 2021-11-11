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


class LessWrong:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['lesswrong']['rate_limit'] / 1000
        # https://www.lesswrong.com/users/{username}
        self.format = config['plateform']['lesswrong']['format']
        # LessWrong usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # forum
        self.type = config['plateform']['lesswrong']['type']

    # Generate all potential lesswrong usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        lesswrong_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to lesswrong")

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
                    user_username = str(
                        soup.find_all(class_="UsersProfile-usernameTitle")[0].get_text()) if soup.find_all(
                        class_="UsersProfile-usernameTitle") else None
                    user_bio = str(soup.find_all(class_="UsersProfile-bio")[0].get_text()) if soup.find_all(
                        class_="UsersProfile-bio") else None

                    account["username"] = {"name": "Username", "value": user_username}
                    account["bio"] = {"name": "Bio", "value": user_bio}
                except:
                    pass

                # Append the account to the accounts table
                lesswrong_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return lesswrong_usernames
