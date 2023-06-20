import logging
import re
import xmlrpc.client

from APIConnection import OdooApi
from databaseAcces import Database

logging.basicConfig(level=logging.DEBUG, filename='logRecords.log', format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

class Fetcher:
    def __init__(self):
        self.OdooApi = OdooApi()
        self.database = Database()

    def fetch(self, table:str, fields=[]) -> bool:
        # By default, fields is empty so all the fields will be retrieved but if
        # someone ask for specific fields and omit id field which is the PRIMARY KEY, it'll add it automatically.
        if len(fields) != 0 and 'id' not in fields: fields.append('id')
        if len(fields) != 0 and '__last_update' not in fields: fields.append('__last_update')

        # Add fields already present in database to update values
        fields = list(set(fields) | set(self.database.getFieldsByName(table)))

        # Verify if table and fields exist
        try:
            field_verification = self.OdooApi.getTableRecords(table=table.replace("_", "."), fields=fields, limit=1)
        except xmlrpc.client.Fault as fault:
            fault = fault.__str__()
            match fault[7]:
                # Fault 1 is field error
                case "1":
                    regex = "ValueError: Invalid field \\\\'.*\\\\' on model \\\\'.*\\\\'"
                    logging.error(re.findall(regex ,fault.__str__())[0].replace("\\'", "") + ". Fetching canceled")
                # Fault 2 is table error
                case "2":
                    logging.error(f"Table {table} doesn't exist. Fetching canceled")
            return False

        # Retrieve fields info and remove useless fields
        fields_info = self.OdooApi.getTableFieldsInfo(table)
        fields_info = [field for field in fields_info if field['name'] in list(field_verification[0].keys())]

        # Retrieve data
        data = self.OdooApi.getTableRecords(table=table.replace("_", "."))

        # Upsert
        self.database.upsert(table, data, fields_info)
