DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    currency TEXT,
    reason TEXT
);

INSERT INTO account VALUES (NULL, 'First demo account', 'ruble', 'contract/100');
INSERT INTO account VALUES (NULL, 'Second demo account', 'ruble', 'contract/101');
