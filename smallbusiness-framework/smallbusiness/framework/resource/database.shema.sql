DROP TABLE IF EXISTS bank;


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

INSERT INTO bank VALUES (1, 'First Demo Bank', '1', '1', '1', '1');


DROP TABLE IF EXISTS partner;

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

INSERT INTO partner VALUES (1, 'First demo partner', 'Moskov City', 'triplustri@mail.ru', '1', '1', 0, '1');
INSERT INTO partner VALUES (2, 'Second demo partner', 'New York City', 'triplustri@mail.ru', '1', '1', 0, '1');


DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    currency_unit_id INTEGER,
    reason TEXT,
    provider_id INTEGER,
    purchaser_id INTEGER,
    date INTEGER
);

INSERT INTO account VALUES (1, 'ruble', 'contract/100', 1, 2, 1);
INSERT INTO account VALUES (NULL, 'ruble', 'contract/101', 2, 1, 1);


DROP TABLE IF EXISTS account_product;

CREATE TABLE account_product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    time_unit_id INTEGER,
    value REAL,
    price REAL,
    account_id INTEGER
);

INSERT INTO account_product VALUES (NULL, 'IT services', 1, 160, 600, 1);
INSERT INTO account_product VALUES (NULL, 'IT services', 1, 160, 600, 1);


DROP TABLE IF EXISTS time_unit;

CREATE TABLE time_unit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

INSERT INTO time_unit VALUES (NULL, 'Hour');
INSERT INTO time_unit VALUES (NULL, 'Day');


DROP TABLE IF EXISTS currency_unit;

CREATE TABLE currency_unit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    code TEXT
);

INSERT INTO currency_unit VALUES (NULL, 'Ruble', 'ruble');
INSERT INTO currency_unit VALUES (NULL, 'Dollar', 'dollar');
INSERT INTO currency_unit VALUES (NULL, 'Euro', 'euro');
