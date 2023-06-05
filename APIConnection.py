import asyncio
import xmlrpc.client
from ConfigLoader import ConfigLoader
"""
config = ConfigLoader().load()

uid = xmlrpc.client.ServerProxy(f"{config.apiURL}/xmlrpc/2/common").authenticate(config.apiDB, config.apiUsername, config.apiPassword, {})

models = xmlrpc.client.ServerProxy(f"{config.apiURL}/xmlrpc/2/object")
"""


class OdooApi:
    def __init__(self):
        self.conf = ConfigLoader().load()
        self.uid = xmlrpc.client.ServerProxy(f"{self.conf.apiURL}/xmlrpc/2/common").authenticate(self.conf.apiDB,
                                                                                                 self.conf.apiUsername,
                                                                                                 self.conf.apiPassword,
                                                                                                 {})
        self.models = xmlrpc.client.ServerProxy(f"{self.conf.apiURL}/xmlrpc/2/object")

    def getAllTables(self):
        tables = self.models.execute_kw(self.conf.apiDB, self.uid, self.conf.apiPassword, 'ir.model', 'search_read', [[['model', '!=', False]]], {'fields': ['model']})
        return tables

    def getTableFieldsInfo(self, table: str):
        """
        Get name, type, description and relation of the specified table.
        :param table:
        :return: List
        """
        fields = self.models.execute_kw(self.conf.apiDB, self.uid, self.conf.apiPassword, 'ir.model.fields', 'search_read', [[['model', '=', table], ['store', '=', True]]], {'fields': ['name', 'relation', 'field_description', 'ttype']})
        return fields

    def getTableData(self, table: str, limit: int = 0):
        ids = self.models.execute_kw(self.conf.apiDB, self.uid, self.conf.apiPassword, table, 'search', [[['id', '>', '0']]], {'limit': limit})
        records = self.models.execute_kw(self.conf.apiDB, self.uid, self.conf.apiPassword, table, 'read', [ids])
        return records

print(OdooApi().getTableData('account.account'))