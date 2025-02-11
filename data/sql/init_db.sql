CREATE TABLE IF NOT EXISTS categories (
	id INTEGER PRIMARY KEY,
	label TEXT NOT NULL UNIQUE,
	properties_template TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS objects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INTEGER NOT NULL,
	properties TEXT NOT NULL
);

INSERT INTO categories (id, label, properties_template)
SELECT 1, "Jeux Video", "manufacturer,platform,title,editor,zone,support,type,release year,condition,status,misc"
WHERE NOT EXISTS(SELECT 1 FROM categories WHERE id=1);

INSERT INTO categories (id, label, properties_template)
SELECT 2, "BDs/Mangas", "author,title,volume,language,publisher,first publication year,publication year,condition,status"
WHERE NOT EXISTS(SELECT 1 FROM categories WHERE id=2);

INSERT INTO categories (id, label, properties_template)
SELECT 3, "Livres Divers", "author,title,language,publisher,first publication year,publication year,condition,status"
WHERE NOT EXISTS(SELECT 1 FROM categories WHERE id=3);
