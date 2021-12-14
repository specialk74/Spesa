DROP TABLE IF EXISTS spesa;

CREATE TABLE spesa (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL,
	quantity INT NOT NULL,
	category INT NOT NULL,
	count INT NOT NULL,
	toTake BOOLEAN NOT NULL
);


INSERT INTO spesa (name, quantity, category, count, toTake) VALUES (
	"Pane", 3, 0, 0, 0
);

INSERT INTO spesa (name, quantity, category, count, toTake) VALUES (
	"Latte", 1, 0, 0, 1
);
