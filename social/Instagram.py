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


class Instagram:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['instagram']['rate_limit'] / 1000
        # https://instagram.com/{username}
        self.format = config['plateform']['instagram']['format']
        self.permutationsList = permutationsList
        # social
        self.type = config['plateform']['instagram']['type']

    # Generate all potential instagram usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        instagram_usernames = {
            "type": self.type,
            "accounts": []
        }

        bibliogram_URL = "https://bibliogram.art/u/{}"

        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                bibliogram_formatted_URL = bibliogram_URL.format(username.replace("https://instagram.com/", ""))
                r = requests.get(bibliogram_formatted_URL)

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
                        user_full_name = str(soup.find_all(class_='full-name')[0].get_text()).strip()
                        user_username = str(soup.find_all(class_='username')[0].get_text()).strip()
                        user_bio = str(soup.find_all(class_='bio')[0].get_text()).replace("\n", "").strip()
                        user_posts_count = str(soup.find_all(class_='count')[0].get_text().replace(",", "")).strip()
                        user_following_count = str(soup.find_all(class_='count')[1].get_text().replace(",", "")).strip()
                        user_followers_count = str(soup.find_all(class_='count')[2].get_text().replace(",", "")).strip()

                        account["full_name"] = {"name": "Full Name", "value": user_full_name}
                        account["username"] = {"name": "Username", "value": user_username}
                        account["bio"] = {"name": "Bio", "value": user_bio}
                        account["posts_count"] = {"name": "Posts", "value": user_posts_count}
                        account["following_count"] = {"name": "Following", "value": user_following_count}
                        account["followers_count"] = {"name": "Followers", "value": user_followers_count}

                    except:
                        self.log.error(f'Error en la búsqueda de información de {username} en instagram')

                    # Append the account to the accounts table
                    instagram_usernames["accounts"].append(account)

            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a instagram')

            time.sleep(self.delay)

        return instagram_usernames
