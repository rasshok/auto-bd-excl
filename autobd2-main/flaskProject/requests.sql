CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_number TEXT NOT NULL,
    date_added TEXT NOT NULL,
    car_type TEXT NOT NULL,
    car_model TEXT NOT NULL,
    problem_description TEXT,
    client_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    status TEXT NOT NULL,
    assigned_mechanic TEXT
);
