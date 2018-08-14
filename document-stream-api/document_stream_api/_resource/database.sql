DROP TABLE IF EXISTS account;

CREATE TABLE account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date INTEGER
);

INSERT INTO account VALUES (NULL, 'First demo account', 0);
INSERT INTO account VALUES (NULL, 'Second demo account', 0);
