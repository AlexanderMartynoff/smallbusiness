from os.path import dirname, abspath


APPLICATION_DIR = dirname(abspath(__file__))
RESOURCE_DIR = f'{APPLICATION_DIR}/_resource'
SQLITE3_DB = f'{RESOURCE_DIR}/database.sqlite3'
