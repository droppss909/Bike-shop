CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    version INTEGER DEFAULT 0
);

CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    price VARCHAR(20) NOT NULL
);

CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) NOT NULL,
    date VARCHAR(20) NOT NULL,
    services INTEGER[],
    posted BOOLEAN NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) NOT NULL,
    bike_id INTEGER REFERENCES bikes(id) NOT NULL,
    posted BOOLEAN NOT NULL
);

CREATE TABLE bills (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) NOT NULL,
    price VARCHAR(5) NOT NULL,
    appointment_ids INTEGER[],
    orders_ids INTEGER[],
    document_title TEXT,
    bill_content TEXT
);

CREATE TABLE bikes (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(10) NOT NULL,
    model VARCHAR(20) NOT NULL,
    year VARCHAR(5) NOT NULL,
    price VARCHAR(5) NOT NULL,
    equipment VARCHAR(20) NOT NULL,
    color VARCHAR(10),
    version INTEGER DEFAULT 0
);

