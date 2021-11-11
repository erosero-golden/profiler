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


class Github:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['github']['rate_limit'] / 1000
        # https://github.com/{username}
        self.format = config['plateform']['github']['format']
        self.permutationsList = permutationsList
        # programming
        self.type = config['plateform']['github']['type']

    # Generate all potential github usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        github_usernames = {
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
                        user_full_name = str(soup.find_all(class_='vcard-fullname')[0].get_text()).strip()
                        user_followers_count = str(
                            soup.find_all(class_='text-bold color-text-primary')[0].get_text().replace(",", "")).strip()
                        user_following_count = str(
                            soup.find_all(class_='text-bold color-text-primary')[1].get_text().replace(",", "")).strip()
                        user_stars_count = str(
                            soup.find_all(class_='text-bold color-text-primary')[2].get_text().replace(",", "")).strip()
                        user_org = str(soup.find_all(class_='p-org')[0].get_text()).strip() if soup.find_all(
                            class_='p-org') else None
                        user_website = str(
                            soup.find_all("li", {"data-test-selector": "profile-website-url"})[0].find_all("a")[
                                0].get_text()) if soup.find_all("li",
                                                                {"data-test-selector": "profile-website-url"}) else None
                        user_twitter = str(
                            soup.find_all("li", {"itemprop": "twitter"})[0].find_all("a")[
                                0].get_text()) if soup.find_all(
                            "li", {"itemprop": "twitter"}) else None
                        user_location = str(soup.find_all("li", {"itemprop": "homeLocation"})[0].find_all("span")[
                                                0].get_text()) if soup.find_all("li",
                                                                                {"itemprop": "homeLocation"}) else None

                        account["full_name"] = {"name": "Full Name", "value": user_full_name}
                        account["followers_count"] = {"name": "Followers", "value": user_followers_count}
                        account["following_count"] = {"name": "Following", "value": user_following_count}
                        account["stars_count"] = {"name": "stars", "value": user_stars_count}
                        account["org"] = {"name": "Organization", "value": user_org}
                        account["website"] = {"name": "Website", "value": user_website}
                        account["twitter"] = {"name": "Twitter", "value": user_twitter}
                        account["location"] = {"name": "Location", "value": user_location}

                    except:
                        self.log.error(f'Error en la búsqueda de información de {username} en aboutme')

                    # Append the account to the accounts table
                    github_usernames["accounts"].append(account)

            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a github')

            time.sleep(self.delay)

        return github_usernames
