"""
Create tables: person, user
"""

from yoyo import step

__depends__ = {'20181206_02_Vpc2b-create-tables-account-product-time-unit'}

steps = [
    step("""
        CREATE TABLE person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mail TEXT,
            position TEXT
        );
    """,

    """
        DROP TABLE IF EXISTS person;
    """),

    step("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            person_id INTEGER
        );
    """,

    """
        DROP TABLE IF EXISTS user;
    """),
]
