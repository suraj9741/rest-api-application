CREATE TABLE IF NOT EXISTS student (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    date_of_birth DATE,
    gender VARCHAR(10)
);