import xmlrpc.client

# Informations de connexion
url = "https://tecliberp-cemineu-v16-upgrade-7592180.dev.odoo.com"
db = "tecliberp-cemineu-v16-upgrade-7592180"
username = "admin"
password = "OLNhrDVKEQfJY"

# Connexion à l'instance Odoo
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

# Création de l'objet pour accéder à l'API Odoo
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Obtention de la liste des tables SQL
tables = models.execute_kw(db, uid, password, 'ir.model', 'search_read', [[['model', '!=', False]]], {'fields': ['model']})

# Obtention des clés primaires et clés étrangères pour chaque table
for table in tables:
    table_name = table['model']
    fields = models.execute_kw(db, uid, password, 'ir.model.fields', 'search_read', [[['model', '=', table_name], ['store', '=', True]]], {'fields': ['name', 'relation', 'field_description']})
    primary_keys = [field['name'] for field in fields if field['relation'] == False]
    foreign_keys = [field for field in fields if field['relation'] != False]

    print(f"Table: {table_name}")
    print(f"Clés primaires: {primary_keys}")
    print("Clés étrangères:")

    # Récupération des informations de la clé étrangère
    for foreign_key in foreign_keys:
        column_name = foreign_key['name']
        destination_table = foreign_key['relation']
        origin_table = models.execute_kw(db, uid, password, 'ir.model.fields', 'search_read', [[['model', '=', destination_table], ['relation', '=', table_name]]], {'fields': ['name']})
        origin_column = origin_table[0]['name'] if origin_table else None

        print(f"  Colonne: {column_name}")
        print(f"  Table d'origine: {table_name}")
        print(f"  Table de destination: {destination_table}")
        print(f"  Colonne d'origine correspondante: {origin_column}")
        print()

    print()
