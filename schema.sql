DROP TABLE IF EXISTS coffees;

CREATE TABLE coffees
(
    coffee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT
);

INSERT INTO coffees (name, price, description)
VALUES 
    ('Americano', 5.00, 'just an ordinary black coffee.'),
    ('Cappuccino', 5.30, 'Coffee and milk'),
    ('Iced Chai Latte', 4.3, 'Steamed milk with black tea, infused with cloves and other yummy spices. Also iced'),
    ('Mocha', 4.20, 'Chocolate and milk and coffee!!!!'),
    ('Hot Chocolate', 5.00, 'Chocolate and milk, so yummy!'),
    ('Pumpkin Flavoured Mocha', 4, 'Mocha with a bit of autumn sprinkled in.'),
    ('Chocolate Orange Latte', 5.20, 'Funky orange zest in a latte!')
    ;

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);