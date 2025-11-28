from DB.db import create_connection

def add_book(title, author):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author) VALUES (%s, %s)",
        (title, author)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Added book: {title}")


def view_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def update_book(book_id, title=None, author=None):
    conn = create_connection()
    cursor = conn.cursor()

    if title:
        cursor.execute("UPDATE books SET title=%s WHERE id=%s", (title, book_id))
    if author:
        cursor.execute("UPDATE books SET author=%s WHERE id=%s", (author, book_id))

    conn.commit()
    cursor.close()
    conn.close()
    print(f" Updated book ID {book_id}")


def safe_delete_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM loan WHERE book_id=%s AND return_date IS NULL",
        (book_id,)
    )
    active_loans = cursor.fetchone()[0]

    if active_loans > 0:
        print(" Cannot delete book — it's currently borrowed!")
    else:
        cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        print(" Book deleted successfully")

    cursor.close()
    conn.close()


def check_book_availability(book_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if book exists
    cursor.execute("SELECT id, title FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        cursor.close()
        conn.close()
        return None, None

    # Check if loan exists
    cursor.execute("""
        SELECT friends.name
        FROM loan
        JOIN friends ON loan.friend_id = friends.id
        WHERE loan.book_id = %s AND loan.return_date IS NULL
    """, (book_id,))

    borrower = cursor.fetchone()

    cursor.close()
    conn.close()

    if borrower is None:
        return True, None
    else:
        return False, borrower[0]
