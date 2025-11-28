from DB.db import create_connection
from datetime import date

def is_book_available(book_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM loan WHERE book_id = %s AND return_date IS NULL",
        (book_id,)
    )
    borrowed_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE id=%s", (book_id,))
    exists = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return exists > 0 and borrowed_count == 0


def borrow_book(book_id, friend_id):
    if not is_book_available(book_id):
        print(" Book already borrowed!")
        return

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO loan (book_id, friend_id, loan_date)
        VALUES (%s, %s, %s)
    """, (book_id, friend_id, date.today()))

    conn.commit()
    cursor.close()
    conn.close()

    print(" Borrowed successfully!")


def return_book(loan_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE loan 
        SET return_date = %s
        WHERE id = %s AND return_date IS NULL
    """, (date.today(), loan_id))

    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()

    if affected > 0:
        print(" Book returned!")
    else:
        print(" Book was already returned or loan ID not found!")


def delete_loan(loan_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM loan WHERE id=%s", (loan_id,))
    conn.commit()

    cursor.close()
    conn.close()
    print(" Loan entry deleted")


def view_loans():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT loan.id, books.title, friends.name, loan.loan_date, loan.return_date
        FROM loan
        JOIN books ON loan.book_id = books.id
        JOIN friends ON loan.friend_id = friends.id
        ORDER BY loan.id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def view_active_loans():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT loan.id, books.title, friends.name, loan.loan_date
        FROM loan
        JOIN books ON loan.book_id = books.id
        JOIN friends ON loan.friend_id = friends.id
        WHERE loan.return_date IS NULL
        ORDER BY loan.loan_date DESC
    """)

    loans = cursor.fetchall()

    cursor.close()
    conn.close()

    return loans
