CREATE TABLE users (
    uID INT UNIQUE,
    userName VARCHAR PRIMARY KEY,
    password VARCHAR,
    role INT
);

CREATE TABLE cities (
    cID INT UNIQUE,
    name VARCHAR PRIMARY KEY
);

CREATE TABLE ads (
    adID INT UNIQUE,
    title VARCHAR,
    content VARCHAR,
    author VARCHAR,
    city VARCHAR,
    FOREIGN KEY (author) REFERENCES users (userName),
    FOREIGN KEY (city) REFERENCES cities (name)
);
