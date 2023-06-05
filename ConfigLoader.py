from dotenv import dotenv_values
import configparser


class ConfigLoader:
    def __init__(self):
        self.apiUsername: str = ""
        self.apiPassword = 0
        self.apiDB = 0
        self.apiURL = 0

        return

    def load(self):
        defaultConf = dotenv_values()
        conf = configparser.ConfigParser()
        conf.read("config.ini")

        api_username = conf['API']['username']
        self.apiUsername = api_username if len(api_username) > 0 else defaultConf['API_USERNAME']

        api_password = conf['API']['password']
        self.apiPassword = api_password if len(api_password) > 0 else defaultConf['API_PASSWORD']

        api_database = conf['API']['database']
        self.apiDB = api_database if len(api_database) > 0 else defaultConf['API_DATABASE']

        api_url = conf['API']['url']
        self.apiURL = api_url if len(api_url) > 0 else defaultConf['API_URL']

        return self
