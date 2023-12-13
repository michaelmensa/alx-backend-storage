-- sql script that creates users with these requirements
-- id: int, never null, auto increment, primary key
-- email: string(255 char), never null, unique
-- name: string(255 char)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
