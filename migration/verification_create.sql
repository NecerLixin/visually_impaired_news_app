CREATE TABLE verification (
    verify_id INTEGER PRIMARY KEY,
    verify_code TEXT(32),
    user_account TEXT(32),
    time DATETIME
);
