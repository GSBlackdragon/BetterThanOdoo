import logging
import random

import pyodbc
from ConfigLoader import ConfigLoader

import time
import random

logging.basicConfig(level=logging.DEBUG, filename='logRecords.log', format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

class TypeMapper:
    def __init__(self):
        self.type_map = {
            'INT': ['int', 'one2many', 'many2one', 'many2many'],
            'VARCHAR(MAX)': ['varchar', 'char', 'selection'],
            'DATETIME': ['datetime', 'date'],
            'BIT': ['boolean'],
            'DECIMAL': ['float', 'monetary']
        }

    def getType(self, given_type):
        for key, values in self.type_map:
            if given_type in values: return key
        logging.error(f"Type {given_type} as no match in type_map and can't be resolve as a SQL server type")
        raise TypeError(f"{given_type} is not a suitable type for SQL server")


class Database:
    def __init__(self):
        # Database connection
        self.conf = ConfigLoader().load().database
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+self.conf.server+';DATABASE='+self.conf.DB+';ENCRYPT=no;UID='+self.conf.username+';PWD='+self.conf.password)
        logging.info(f"Connected to database : username={self.conf.username}, server={self.conf.server}, database={self.conf.DB}")
        self.cursor = self.conn.cursor()
        self.cursor.fast_executemany = True
        # Handle type difference between Odoo's API and SQL Server
        self.typeMapper = TypeMapper()

    def query(self, query, commit=False):
        query_result = self.cursor.execute(query)
        if commit: self.commit()
        return query_result

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def getFieldsByName(self, table):
        fields_name = self.query(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';").fetchall()
        fields_name = [field[0] for field in fields_name]
        return fields_name

    def insert(self, table, data):
        self.cursor.execute()

    def upsert(self, table, data: list[dict], fields_info):
        # sorting fields_info and data
        fields_info = sorted(fields_info, key=lambda d: d['name'])
        data = [dict(sorted(value.items())) for value in data]

        # Create table if it doesn't exist
        if self.query(f"SELECT * FROM TEST_BTO.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = '{table}'").fetchone() is None:
            self.query(f"CREATE TABLE {table} (id INT CONSTRAINT PRIMARY KEY, __last_update DATETIME)")

        # Add fields that doesn't exist
        existing_fields = self.getFieldsByName(table)

        for field in fields_info:
            if field['name'] not in existing_fields:
                self.query(f"ALTER TABLE {table} ADD {field['name']} {self.typeMapper.getType(field['ttype'])}")

        ids_and_update = self.query(f"SELECT id, __last_update FROM {table}").fetchall()

        # Inserting or Updating data



db = Database()

