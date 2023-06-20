from dotenv import dotenv_values
import configparser


class APIConfigData:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.DB = ""
        self.url = ""

class DatabaseConfigData:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.DB = ""
        self.server = ""

class ConfigLoader:
    def __init__(self):
        # API
        self.API = APIConfigData()
        self.database = DatabaseConfigData()

        # Database

    def load(self):
        # Reading .ini file
        default_conf = dotenv_values()
        conf = configparser.ConfigParser()
        conf.read("config.ini")

        # API
        api_username = conf['API']['username']
        self.API.username = api_username if len(api_username) > 0 else default_conf['API_USERNAME']

        api_password = conf['API']['password']
        self.API.password = api_password if len(api_password) > 0 else default_conf['API_PASSWORD']

        api_database = conf['API']['database']
        self.API.DB = api_database if len(api_database) > 0 else default_conf['API_DATABASE']

        api_url = conf['API']['url']
        self.API.url = api_url if len(api_url) > 0 else default_conf['API_URL']

        #database
        db_username = conf['DATABASE']['username']
        self.database.username = db_username

        db_password = conf['DATABASE']['password']
        self.database.password = db_password

        db_database = conf['DATABASE']['database']
        self.database.DB = db_database

        db_server = conf['DATABASE']['server']
        self.database.server = db_server

        return self
