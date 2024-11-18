CREATE TABLE User (
    id CHAR(36) PRIMARY KEY, -- UUID format
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY, -- UUID format
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL, -- Foreign key referencing User(id)
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES
('123e4567-e89b-12d3-a456-426614174000', 'John', 'Doe', 'john.doe@example.com', 'hashed_password', FALSE);
