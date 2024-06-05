CREATE TABLE audio (
    audio_id INTEGER PRIMARY KEY,
    news_id INTEGER,
    audio_title BLOB,
    audio_content BLOB,
    FOREIGN KEY (news_id) REFERENCES News(news_id)
);
