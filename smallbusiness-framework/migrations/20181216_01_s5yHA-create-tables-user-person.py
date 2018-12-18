"""
create tables: user, person
"""

from yoyo import step

__depends__ = {'20181206_02_Vpc2b-create-tables-account-product-time-unit'}

steps = [
    step("""
        CREATE TABLE person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            mail TEXT,
            address TEXT
        );
    """,
    """
        DROP TABLE IF EXISTS person;
    """),

    step("""
        INSERT INTO person VALUES (1, 'Jhohn Dow', 'Administrator', 'jhohn.dow@smallbusiness.com', NULL);
    """),

    step("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            password TEXT,
            person_id INTEGER
        );
    """,

    """
        DROP TABLE IF EXISTS user;
    """),

    step("""
        INSERT INTO user VALUES (NULL, 'admin', 'admin', 1);
    """),
]
