import logging
import re
import time
import xmlrpc.client
from ConfigLoader import ConfigLoader

logging.basicConfig(level=logging.DEBUG, filename='logRecords.log',
                    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


def getTableFieldsName(fields_info: dict) -> list:
    return [field['name'] for field in fields_info]


class OdooApi:
    def __init__(self):
        self.conf = ConfigLoader().load().API
        self.uid = xmlrpc.client.ServerProxy(f"{self.conf.url}/xmlrpc/2/common").authenticate(self.conf.DB,
                                                                                              self.conf.username,
                                                                                              self.conf.password,
                                                                                              {})
        logging.info("Connected to Odoo API")
        self.models = xmlrpc.client.ServerProxy(f"{self.conf.url}/xmlrpc/2/object")

    def getAllTables(self):
        tables = self.models.execute_kw(self.conf.DB, self.uid, self.conf.password, 'ir.model', 'search_read',
                                        [[['model', '!=', False]]], {'fields': ['model']})
        return tables

    def getTableFieldsInfo(self, table: str) -> dict:
        """
        Get name, type, description and relation of the specified table.
        :param table:
        :return: List
        """
        fields = self.models.execute_kw(self.conf.DB, self.uid, self.conf.password, 'ir.model.fields', 'search_read',
                                        [[['model', '=', table]]],
                                        {'fields': ['name', 'relation', 'field_description', 'ttype']})
        return fields

    def getTableRecords(self, table: str, fields: list = [], limit: int = 0):
        """
        Get a table, a number of row and the fields you want and return table data\n
        By default, it'll return all the records with all fields
        :param table: str
        :param limit: int
        :param fields: list[str]
        :return: list[dict]
        """
        ids = self.models.execute_kw(self.conf.DB, self.uid, self.conf.password, table, 'search', [[['id', '>', '0']]],
                                     {'limit': limit})
        records = self.models.execute_kw(self.conf.DB, self.uid, self.conf.password, table, 'read', [ids],
                                         {'fields': fields})
        return records


"""
odoo = OdooApi()
tables = odoo.getAllTables()
no_write_date = []
for table in tables:
    fields = odoo.getTableFieldsInfo(table['model'])
    here = False
    for field in fields:
        if field['name'] == '__last_update':
            here = True
            break
    if not here: no_write_date.append(table['model'])

print(f"{len(no_write_date)} tables without write_date :")
for table in no_write_date:
    print(table)
"""
odoo = OdooApi()


tables = ["calendar.event", "account.tax", "account.payment.term", "account.move.line", "account.journal", "account.fiscal.position", "account.analytic.account", "x__bi__sql__view.res__partner__res__partner__category__rel", "purchase.order.line", "x__bi__sql__view.meeting__category__rel", "mail.message", "uom.uom", "stock.location", "res.users", "res.partner.category", "res.partner", "res.currency", "purchase.order", "product.template", "product.product", "product.pricelist.item", "product.pricelist", "crm.team", "crm.lead"]

for table in tables:
    try:
        data = odoo.getTableRecords(table)
        print(f"{table} : {len(data)}")
    except:
        print(f"{table} : throw a error")

