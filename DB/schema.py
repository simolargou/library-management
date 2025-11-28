from db import create_connection, create_database_if_missing

def create_tables():
    create_database_if_missing()
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    queries = [
        "DROP TABLE IF EXISTS loan;",
        "DROP TABLE IF EXISTS friends;",
        "DROP TABLE IF EXISTS books;",

        """
        CREATE TABLE books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL
        );
        """,

        """
        CREATE TABLE friends (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(30) UNIQUE,
            email VARCHAR(255) UNIQUE
        );
        """,

        """
        CREATE TABLE loan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            friend_id INT NOT NULL,
            loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            return_date DATETIME,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (friend_id) REFERENCES friends(id)
        );

        """
    ]

    for q in queries:
        cursor.execute(q)

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables created successfully!")


if __name__ == "__main__":
    create_tables()
