CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50),
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    feedback_id INT REFERENCES feedback(id),
    category VARCHAR(50),
    priority VARCHAR(10),
    summary TEXT,
    processed_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO feedback (source, text) VALUES
 ('github', 'The API returns 500 when payload is over 1MB'),
 ('email', 'Would love dark mode in the dashboard'),
 ('form', 'Cannot export data to CSV — button does nothing'),
 ('github', 'Performance is really slow on mobile devices'),
 ('email', 'Great product overall, just needs better docs'),
 ('form', 'The login page takes 10 seconds to load on Chrome'),
 ('email', 'Can you add a way to import users from Excel?'),
 ('github', 'Found a typo in the API documentation on page 5'),
 ('form', 'The app crashes when I click the "Forgot Password" link');
