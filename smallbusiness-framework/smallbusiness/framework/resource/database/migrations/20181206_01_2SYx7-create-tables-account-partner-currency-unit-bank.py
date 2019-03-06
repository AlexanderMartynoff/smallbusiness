"""
Create tables: account, partner, currency_unit, bank
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_unit_id INTEGER,
            reason TEXT,
            provider_id INTEGER,
            purchaser_id INTEGER,
            date INTEGER
        );
    """,

    """
        DROP TABLE IF EXISTS account;
    """),

    step("""
        CREATE TABLE bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            -- ИНН
            taxpayer_number TEXT,
            -- КПП
            reason_code TEXT,
            -- БИК
            identity_code TEXT,
            -- КОРСЧЕТ
            correspondent_account TEXT
        );
    """,

    """
        DROP TABLE IF EXISTS bank;
    """),

    step("""
        CREATE TABLE partner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            mail TEXT,
            taxpayer_number TEXT,
            reason_code TEXT,
            bank_id INTEGER,
            -- ЛИЦСЧЕТ
            bank_checking_account TEXT
        );
    """,

    """
        DROP TABLE IF EXISTS partner;
    """),

    step("""
        CREATE TABLE currency_unit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            code TEXT
        );
    """,

    """
        DROP TABLE IF EXISTS currency_unit;
    """),

    step("""
        INSERT INTO currency_unit VALUES (NULL, 'Euro', 'euro');
    """),

    step("""
        INSERT INTO currency_unit VALUES (NULL, 'Ruble', 'ruble');
    """),

    step("""
        INSERT INTO currency_unit VALUES (NULL, 'Dollar', 'dollar');
    """),
]
