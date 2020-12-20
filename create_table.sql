CREATE TABLE Users (
    userId int UNIQUE NOT NULL,
    username varchar(50) NOT NULL PRIMARY KEY,
    password varchar(250) NOT NULL,
    role int NOT NULL
);



CREATE TABLE Cities (
    cityId int UNIQUE NOT NULL,
    cityname varchar(50) NOT NULL PRIMARY KEY
);

CREATE TABLE Ads (
    adId int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    title varchar(50) NOT NULL,
	content varchar(250) NOT NULL,
	author varchar(50) NOT NULL FOREIGN KEY REFERENCES Users(username),
    city varchar(50) NOT NULL FOREIGN KEY REFERENCES Cities(cityname),
);
