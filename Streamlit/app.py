import sys
import os

# Ensure project root is importable
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

import streamlit as st

# Services

from Services.books import (
    view_books,
    add_book,
    update_book,
    safe_delete_book,
    check_book_availability,
    get_book
)
from Services.friends import (
    view_friends,
    add_friend,
    update_friend,
    safe_delete_friend,
    get_friend_loans,
    search_friend,
    get_friend
)
from Services.loan import (
    view_loans,
    view_active_loans,
    borrow_book,
    return_book,
    delete_loan
)

# HELPER DROPFOWN

def get_books_dropdown():
    books = view_books()
    return {f"{b[1]} (ID {b[0]})": b[0] for b in books}

def get_friends_dropdown():
    friends = view_friends()
    return {f"{f[1]} (ID {f[0]})": f[0] for f in friends}

def get_active_loans_dropdown():
    loans = view_active_loans()
    return {f"{l[1]} - {l[2]} (Loan {l[0]})": l[0] for l in loans}

def get_all_loans_dropdown():
    loans = view_loans()
    return {f"{l[1]} - {l[2]} (Loan {l[0]})": l[0] for l in loans}

# HELPERS HEARDERS 

def friends_table():
    rows = view_friends()
    return {
        "ID": [r[0] for r in rows],
        "Name": [r[1] for r in rows],
        "Phone": [r[2] for r in rows],
        "Email": [r[3] for r in rows]
    }

def books_table():
    rows = view_books()
    return {
        "ID": [r[0] for r in rows],
        "Title": [r[1] for r in rows],
        "Author": [r[2] for r in rows]
    }

def loans_table():
    rows = view_loans()
    return {
        "Loan ID": [r[0] for r in rows],
        "Book": [r[1] for r in rows],
        "Friend": [r[2] for r in rows],
        "Loan Date": [r[3] for r in rows],
        "Return Date": [r[4] for r in rows]
    }

def active_loans_table():
    rows = view_active_loans()
    return {
        "Loan ID": [r[0] for r in rows],
        "Book": [r[1] for r in rows],
        "Friend": [r[2] for r in rows],
        "Loan Date": [r[3] for r in rows]
    }

# UI Setup

st.set_page_config(page_title="Liane Library Dashboard", layout="wide")

st.markdown("""
<style>
    .section-title {
        color: #333;
        font-size: 26px;
        font-weight: 600;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Friends", "Loans", "Books"])

# FRIENDS

if page == "Friends":

    st.markdown("<h1 class='section-title'>Friends Management</h1>", unsafe_allow_html=True)

    tabs = st.tabs([
        "Add Friend",
        "View Friends",
        "Search Friend",
        "Friend Loans",
        "Edit Friend",
        "Delete Friend"
    ])

    # Add Friend
    with tabs[0]:
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")

        if st.button("Save Friend", key="add_friend"):
            if name and phone:
                add_friend(name, phone, email)
                st.success("Friend added.")
            else:
                st.error("Name and phone required.")

    # View Friends
    with tabs[1]:
        st.dataframe(friends_table())

    # Search Friend
    with tabs[2]:
        friends = get_friends_dropdown()
        if friends:
            selected = st.selectbox("Select Friend", list(friends.keys()), key="search_friend")
            friend_id = friends[selected]
            st.dataframe([get_friend(friend_id)], width=800)
        else:
            st.info("No friends available.")

    # Friend Loans
    with tabs[3]:
        friends = get_friends_dropdown()
        if friends:
            selected = st.selectbox("Choose Friend", list(friends.keys()), key="friend_loans")
            friend_id = friends[selected]
            loans = get_friend_loans(friend_id)
            st.dataframe(loans, width=800)
        else:
            st.info("No friends available.")

    # Edit Friend
    with tabs[4]:
        friends = get_friends_dropdown()
        if friends:
            selected = st.selectbox("Select Friend", list(friends.keys()), key="edit_friend")
            friend_id = friends[selected]
            friend = get_friend(friend_id)

            new_name = st.text_input("Name", value=friend[1])
            new_phone = st.text_input("Phone", value=friend[2] or "")
            new_email = st.text_input("Email", value=friend[3] or "")

            if st.button("Save Changes", key="edit_friend_button"):
                update_friend(friend_id, new_name, new_phone, new_email)
                st.success("Friend updated.")
        else:
            st.info("No friends available.")

    # Delete Friend
    with tabs[5]:
        friends = get_friends_dropdown()
        if friends:
            selected = st.selectbox("Select Friend", list(friends.keys()), key="delete_friend")
            friend_id = friends[selected]

            if st.button("Delete Friend", key="delete_friend_button"):
                safe_delete_friend(friend_id)
                st.success("If the friend had no active loans, deletion succeeded.")
        else:
            st.info("No friends available.")

# LOANS

elif page == "Loans":

    st.markdown("<h1 class='section-title'>Loan Management</h1>", unsafe_allow_html=True)

    tabs = st.tabs(["Active Loans", "All Loans", "Borrow Book", "Return Book", "Delete Loan"])

    # Active Loans
    with tabs[0]:
        st.dataframe(active_loans_table())

    # All Loans
    with tabs[1]:
        st.dataframe(loans_table())

    # Borrow Book
    with tabs[2]:
        books = get_books_dropdown()
        friends = get_friends_dropdown()

        if books and friends:
            book_key = st.selectbox("Select Book", list(books.keys()), key="borrow_book_book")
            friend_key = st.selectbox("Select Friend", list(friends.keys()), key="borrow_book_friend")

            if st.button("Borrow", key="borrow_button"):
                borrow_book(books[book_key], friends[friend_key])
                st.success("Loan created.")
        else:
            st.info("No books or friends available.")

    # Return Book
    with tabs[3]:
        loans = get_active_loans_dropdown()
        if loans:
            loan_key = st.selectbox("Select Active Loan", list(loans.keys()), key="return_book")
            if st.button("Return", key="return_button"):
                return_book(loans[loan_key])
                st.success("Book returned.")
        else:
            st.info("No active loans.")

    # Delete Loan
    with tabs[4]:
        loans = get_all_loans_dropdown()
        if loans:
            loan_key = st.selectbox("Select Loan", list(loans.keys()), key="delete_loan")
            if st.button("Delete Loan", key="delete_loan_button"):
                delete_loan(loans[loan_key])
                st.success("Loan deleted.")
        else:
            st.info("No loan records.")

# BOOKS 

elif page == "Books":

    st.markdown("<h1 class='section-title'>Book Management</h1>", unsafe_allow_html=True)

    tabs = st.tabs(["View Books", "Add Book", "Check Availability", "Active Loans", "Edit Book", "Delete Book"])

    # View Books
    with tabs[0]:
        st.dataframe(books_table())

    # Add Book
    with tabs[1]:
        title = st.text_input("Title")
        author = st.text_input("Author")

        if st.button("Save Book", key="add_book"):
            if title and author:
                add_book(title, author)
                st.success("Book added.")
            else:
                st.error("Both fields required.")

    # Check Availability
    with tabs[2]:
        books = get_books_dropdown()
        if books:
            selected = st.selectbox("Select Book", list(books.keys()), key="availability_check")
            book_id = books[selected]

            if st.button("Check", key="availability_button"):
                available, borrower = check_book_availability(book_id)
                if available:
                    st.success("Book is available.")
                else:
                    st.error("Book is borrowed.")
                    st.info(f"Borrowed by: {borrower}")
        else:
            st.info("No books available.")

    # Active Loans
    with tabs[3]:
        st.dataframe(active_loans_table())

    # Edit Book
    with tabs[4]:
        books = get_books_dropdown()
        if books:
            selected = st.selectbox("Select Book", list(books.keys()), key="edit_book")
            book_id = books[selected]
            book = get_book(book_id)

            new_title = st.text_input("Title", value=book[1])
            new_author = st.text_input("Author", value=book[2])

            if st.button("Save Book Changes", key="edit_book_button"):
                update_book(book_id, new_title, new_author)
                st.success("Book updated.")
        else:
            st.info("No books available.")

    # Delete Book
    with tabs[5]:
        books = get_books_dropdown()
        if books:
            selected = st.selectbox("Select Book", list(books.keys()), key="delete_book")
            book_id = books[selected]

            if st.button("Delete Book", key="delete_book_button"):
                safe_delete_book(book_id)
                st.success("If the book was not borrowed, deletion succeeded.")
        else:
            st.info("No books available.")
