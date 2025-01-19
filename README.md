#
pip install -r requirements.txt
#
CREATE DATABASE JodWai;
USE JodWai;

CREATE TABLE account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    lastname VARCHAR(100)
);
CREATE TABLE expense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    description TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES account(email) ON DELETE CASCADE
);
CREATE TABLE hantao_friend (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    email VARCHAR(255) NOT NULL,
    friend_name VARCHAR(255) NOT NULL, 
    amount DECIMAL(10, 2) NOT NULL,
    activity TEXT,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (email) REFERENCES account(email) ON DELETE CASCADE
);
#
