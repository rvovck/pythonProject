CREATE TABLE users (
    uID INT,
    userName VARCHAR PRIMARY KEY,
    password VARCHAR,
    role INT
);

CREATE TABLE cities (
    cID INT,
    name VARCHAR PRIMARY KEY
);

CREATE TABLE ads (
    adID INT,
    title VARCHAR,
    content VARCHAR,
    author VARCHAR,
    city VARCHAR,
    PRIMARY KEY (adID),
    FOREIGN KEY (author) REFERENCES users (userName),
    FOREIGN KEY (city) REFERENCES cities (name)
);
