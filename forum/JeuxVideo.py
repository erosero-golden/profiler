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


class JeuxVideo:

    def __init__(self, config, permutationsList):
        self.log = Logger().getLogger(self.__class__.__name__)
        self.log.info(f"Iniciando búsqueda de [{self.__class__.__name__}] para {permutationsList}")
        # 1000 ms
        self.delay = config['plateform']['jeuxvideo.com']['rate_limit'] / 1000
        # https://www.jeuxvideo.com/profil/{}?mode=infos
        self.format = config['plateform']['jeuxvideo.com']['format']
        # jeuxvideo.com usernames are not case sensitive
        self.permutationsList = [perm.lower() for perm in permutationsList]
        # forum
        self.type = config['plateform']['jeuxvideo.com']['type']

    # Generate all potential 0x00sec usernames
    def possibleUsernames(self):
        possibleUsernames = []

        for permutation in self.permutationsList:
            possibleUsernames.append(self.format.format(
                permutation=permutation,
            ))
        return possibleUsernames

    def search(self):
        jeuxvideo_usernames = {
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

                    # Scrape the user description
                    try:
                        user_description = str(soup.find_all(class_='bloc-description-desc')[0].get_text()).replace(
                            "\n",
                            " ").strip() if soup.find_all(
                            class_='bloc-description-desc') else None
                        account["description"] = {"name": "Description", "value": user_description}
                    except:
                        self.log.error(f'Error en la búsqueda de descripción de {username} en jeuxvideo.com')

                    # scrape the user signature
                    try:
                        user_signature = str(
                            soup.find_all(class_='bloc-signature-desc')[0].find_all("p")[1].get_text()).replace("\n",
                                                                                                                " ").strip() if soup.find_all(
                            class_='bloc-signature-desc') else None
                        account["signature"] = {"name": "Signature", "value": user_signature}
                    except:
                        self.log.error(f'Error en la búsqueda de firma de {username} en jeuxvideo.com')

                    # scrape the user informations
                    try:
                        informations_correspondances = {
                            "Age": "age",
                            "Pays": "country",
                            "Pays / Ville": "country_city",
                            "Genre": "gender",
                            "Membre depuis": "inscription",
                            "Messages Forums": "messages_count",
                            "Commentaires": "comments",
                            "Dernier passage": "last_connection"

                        }

                        user_informations = soup.find_all(class_='bloc-default-profil')[0].find_all("li")
                        for information in user_informations:
                            information = [str(' '.join(info.strip().split())) for info in
                                           information.get_text().split(":")]
                            account[informations_correspondances[information[0]]] = {"name": information[0],
                                                                                     "value": information[1]}

                    except:
                        self.log.error(f'Error en la búsqueda de información adicional de {username} en jeuxvideo.com')

                    # Append the account to the accounts table
                    jeuxvideo_usernames["accounts"].append(account)

            except requests.ConnectionError:
                self.log.error('Error al realizar la petición a jeuxvideo.com')

            time.sleep(self.delay)

        return jeuxvideo_usernames
