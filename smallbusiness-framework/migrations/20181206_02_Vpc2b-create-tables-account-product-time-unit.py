"""
Create tables: account_product, time_unit
"""

from yoyo import step

__depends__ = {'20181206_01_2SYx7-create-tables-account-partner-currency-unit-bank'}


steps = [
    step("""
        CREATE TABLE account_product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            time_unit_id INTEGER,
            value REAL,
            price REAL,
            account_id INTEGER
        );
    """,

    """
        DROP TABLE IF EXISTS account_product;
    """),

    step("""
        CREATE TABLE time_unit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
    """,

    """
        DROP TABLE IF EXISTS time_unit;
    """),

    step("""
        INSERT INTO time_unit VALUES (NULL, 'Day');
    """),

    step("""
        INSERT INTO time_unit VALUES (NULL, 'Hour');
    """),
]
