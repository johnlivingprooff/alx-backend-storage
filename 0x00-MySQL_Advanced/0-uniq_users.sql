-- creating a table for users
-- user table has id, name, email

IF NOT EXISTS (SELECT * FROM information_schema.tables WHERE table_name = 'users') THEN
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
END IF;
