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
import re

from tuteggito.enrich.basics.utils.Logger import Logger


class Flickr:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['flickr']['rate_limit'] / 1000
        # https://flickr.com/photos/{username}
        self.format = config['plateform']['flickr']['format']
        self.permutationsList = permutationsList
        # social
        self.type = config['plateform']['flickr']['type']

    # Generate all potential flickr usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        flickr_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to flickr")

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
                    user_username = str(soup.find_all("div", {"class": "title"})[0].find_all("h1")[
                                            0].get_text().strip()) if soup.find_all("div", {"class": "title"}) else None
                    user_pictures_count = str(
                        soup.find_all("p", {"class": "photo-count"})[0].get_text().split(' ')[0].replace(',',
                                                                                                         '')) if soup.find_all(
                        "p", {"class": "photo-count"}) else None

                    followers = str(soup.find_all("p", {"class": "followers"})[0].get_text()) if soup.find_all("p", {
                        "class": "followers"}) else None
                    user_followers_count = followers.split(' ')[0]
                    user_following_count = followers.split(' ')[1].split('•')[1]

                    account["username"] = {"name": "Username", "value": user_username}
                    account["following_count"] = {"name": "Following", "value": user_following_count}
                    account["followers_count"] = {"name": "Followers", "value": user_followers_count}
                    account["pictures_count"] = {"name": "Pictures", "value": user_pictures_count}
                except:
                    pass

                # Append the account to the accounts table
                flickr_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return flickr_usernames
