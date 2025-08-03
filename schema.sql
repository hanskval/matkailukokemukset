CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE experiences (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    FOREIGN KEY (user_id) REFERENCES users(id)

);
CREATE TABLE likes (
    user_id INTEGER REFERENCES users(id),
    experience_id INTEGER REFERENCES experiences(id),
    PRIMARY KEY (user_id, experience_id)
);
