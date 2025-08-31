CREATE TABLE IF NOT EXISTS JobListings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    link VARCHAR(500) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    salary TEXT
);