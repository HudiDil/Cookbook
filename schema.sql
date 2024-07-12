DROP TABLE IF EXISTS collections;
DROP TABLE IF EXISTS recipes;

CREATE TABLE collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    collection_id INTEGER,
    FOREIGN KEY (collection_id) REFERENCES collections (id)
);