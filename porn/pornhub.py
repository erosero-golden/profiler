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

class Pornhub:

    def __init__(self, config, permutationsList):
        # 1000 ms
        self.delay = config['plateform']['pornhub']['rate_limit'] / 1000
        # https://pornhub.com/users/{username}
        self.format = config['plateform']['pornhub']['format']
        # pornhub usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # porn
        self.type = config['plateform']['pornhub']['type']

    # Generate all potential pornhub usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation = permutation,
            ))
        return possibleUsernames

    def search(self):
        pornhub_usernames = {
            "type": self.type,
            "accounts": []
        }
        possibleUsernames_list = self.possibleUsernames()

        for username in possibleUsernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to pornhub")
            
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
                    user_followers = str(soup.find_all(class_="subViewsInfoContainer")[0].find_all(class_="number")[0].get_text()).strip() if soup.find_all(class_="subViewsInfoContainer") else None
                    user_friends = str(soup.find_all(class_="subViewsInfoContainer")[0].find_all(class_="number")[1].get_text()).strip() if soup.find_all(class_="subViewsInfoContainer") else None
                    user_watch_count = str(soup.find_all(class_="subViewsInfoContainer")[0].find_all(class_="number")[2].get_text()).strip() if soup.find_all(class_="subViewsInfoContainer") else None

                    account["followers"] = {"name": "Followers", "value": user_followers}
                    account["friends"] = {"name": "Friends", "value": user_friends}
                    account["watch_count"] = {"name": "Watched Videos", "value": user_watch_count}
                except:
                    pass
                
                # Append the account to the accounts table
                pornhub_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return pornhub_usernames