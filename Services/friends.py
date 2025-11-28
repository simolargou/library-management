from DB.db import create_connection

def add_friend(name, phone, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO friends (name, phone, email) VALUES (%s, %s, %s)",
        (name, phone, email)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Added friend: {name}")


def view_friends():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, email FROM friends")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_friend(friend_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM friends WHERE id=%s", (friend_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data


def update_friend(friend_id, name=None, phone=None, email=None):
    conn = create_connection()
    cursor = conn.cursor()

    if name:
        cursor.execute("UPDATE friends SET name=%s WHERE id=%s", (name, friend_id))
    if phone:
        cursor.execute("UPDATE friends SET phone=%s WHERE id=%s", (phone, friend_id))
    if email:
        cursor.execute("UPDATE friends SET email=%s WHERE id=%s", (email, friend_id))

    conn.commit()
    cursor.close()
    conn.close()
    print(f" Updated friend ID {friend_id}")


def safe_delete_friend(friend_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM loan WHERE friend_id = %s AND return_date IS NULL",
        (friend_id,)
    )
    active_loans = cursor.fetchone()[0]

    if active_loans > 0:
        print(" Cannot delete friend — they still have borrowed books!")
    else:
        cursor.execute("DELETE FROM friends WHERE id=%s", (friend_id,))
        conn.commit()
        print(" Friend deleted successfully")

    cursor.close()
    conn.close()


def get_friend_loans(friend_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT loan.id, books.title, loan.loan_date, loan.return_date
        FROM loan
        JOIN books ON loan.book_id = books.id
        WHERE loan.friend_id = %s
        ORDER BY loan.loan_date DESC
    """, (friend_id,))

    loans = cursor.fetchall()

    cursor.close()
    conn.close()

    return loans


def search_friend(query):
    conn = create_connection()
    cursor = conn.cursor()

    query = f"%{query}%"

    cursor.execute("""
        SELECT id, name, phone, email
        FROM friends
        WHERE name LIKE %s 
           OR phone LIKE %s
           OR email LIKE %s
    """, (query, query, query))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results
