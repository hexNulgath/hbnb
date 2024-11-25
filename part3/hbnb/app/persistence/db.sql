CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT,
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    CONSTRAINT unique_review_for_place UNIQUE (user_id, place_id),
    CHECK (
        rating BETWEEN 1
        AND 5
    )
);

CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

INSERT INTO
    User (
        id,
        first_name,
        last_name,
        email,
        password,
        is_admin
    )
VALUES
    (
        '123e4567-e89b-12d3-a456-426614174000',
        'John',
        'Doe',
        'john.doe@example.com',
        'hashed_password',
        FALSE
    );

INSERT INTO
    Amenity (id, name)
VALUES
    ('', 'WiFi'),
    ('', 'Swimming Pool'),
    ('', 'Air Conditioning');