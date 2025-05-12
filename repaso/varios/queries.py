ADDRESS_BOOK_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    phone VARCHAR(16),
    email VARCHAR(64),
    birthday DATE
)
"""
ADDRESS_BOOK_INSERT_SQL = """
INSERT INTO contact(name, last_name, phone, email, birthday)
VALUES(?, ?, ?, ?, ?)
"""
ADDRESS_BOOK_DELETE_SQL = """
DELETE FROM contact WHERE id = ?
"""
ADDRESS_BOOK_UPDATE_SQL = """
UPDATE 
    contact
SET 
    name=?,
    last_name=?,
    phone=?,
    email=?,
    birthday=?
WHERE
    id=?
"""
ADDRESS_BOOK_SELECT_ALL_SQL = """
SELECT * FROM contact ORDER BY id ASC
"""
ADDRESS_BOOK_SELECT_SQL = """
SELECT * FROM contact 
WHERE id=?
"""