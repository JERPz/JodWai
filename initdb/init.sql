-- สร้างตาราง account
CREATE TABLE IF NOT EXISTS account (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL
);

-- สร้างตาราง expense
CREATE TABLE IF NOT EXISTS expense (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    type VARCHAR(10) NOT NULL, -- income / expense
    description TEXT,
    date DATE DEFAULT CURRENT_DATE
);

-- สร้างตาราง hantao_friend
CREATE TABLE IF NOT EXISTS hantao_friend (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    friend_name VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    activity TEXT,
    date DATE DEFAULT CURRENT_DATE
);
