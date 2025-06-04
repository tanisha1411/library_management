import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tiamishra1417",
        database="management"
    )

def insert_data(table):
    conn = connect()
    cursor = conn.cursor()

    if table == "Publishers":
        name = input("Enter Publisher Name: ")
        address = input("Enter Publisher Address: ")
        contact = input("Enter Publisher Contact: ")
        cursor.execute("INSERT INTO Publishers (Name, Address, Contact) VALUES (%s, %s, %s)", (name, address, contact))

    elif table == "Books":
        title = input("Enter Book Title: ")
        author = input("Enter Author: ")
        genre = input("Enter Genre: ")
        isbn = input("Enter ISBN: ")
        status = input("Enter Status (Available/Issued): ")
        publisher_id = input("Enter Publisher ID: ")
        cursor.execute("INSERT INTO Books (Title, Author, Genre, ISBN, Status, Publisher_ID) VALUES (%s, %s, %s, %s, %s, %s)", (title, author, genre, isbn, status, publisher_id))

    elif table == "Users":
        name = input("Enter User Name: ")
        email = input("Enter Email: ")
        membership_date = input("Enter Membership Date (YYYY-MM-DD): ")
        user_type = input("Enter User Type (Student/Faculty/Staff): ")
        cursor.execute("INSERT INTO Users (Name, Email, Membership_Date, User_Type) VALUES (%s, %s, %s, %s)", (name, email, membership_date, user_type))

    elif table == "Transactions":
        user_id = input("Enter User ID: ")
        book_id = input("Enter Book ID: ")
        issue_date = input("Enter Issue Date (YYYY-MM-DD): ")
        due_date = input("Enter Due Date (YYYY-MM-DD): ")
        return_date = input("Enter Return Date (YYYY-MM-DD) or leave blank: ")
        cursor.execute("INSERT INTO Transactions (User_ID, Book_ID, Issue_Date, Due_Date, Return_Date) VALUES (%s, %s, %s, %s, %s)", (user_id, book_id, issue_date, due_date, return_date if return_date else None))

    conn.commit()
    cursor.close()
    conn.close()

def view_data(table):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()

def update_data(table):
    conn = connect()
    cursor = conn.cursor()

    if table == "Books":
        book_id = input("Enter Book ID to update: ")
        new_status = input("Enter new status: ")
        cursor.execute("UPDATE Books SET Status = %s WHERE Book_ID = %s", (new_status, book_id))

    elif table == "Users":
        user_id = input("Enter User ID to update: ")
        new_email = input("Enter new email: ")
        cursor.execute("UPDATE Users SET Email = %s WHERE User_ID = %s", (new_email, user_id))

    elif table == "Transactions":
        transaction_id = input("Enter Transaction ID to update: ")
        new_return_date = input("Enter new return date (YYYY-MM-DD): ")
        cursor.execute("UPDATE Transactions SET Return_Date = %s WHERE Transaction_ID = %s", (new_return_date, transaction_id))

    conn.commit()
    cursor.close()
    conn.close()

def delete_data(table):
    conn = connect()
    cursor = conn.cursor()
    record_id = input(f"Enter ID to delete from {table}: ")

    if table == "Books":
        cursor.execute("DELETE FROM Books WHERE Book_ID = %s", (record_id,))
    elif table == "Users":
        cursor.execute("DELETE FROM Users WHERE User_ID = %s", (record_id,))
    elif table == "Publishers":
        cursor.execute("DELETE FROM Publishers WHERE Publisher_ID = %s", (record_id,))
    elif table == "Transactions":
        cursor.execute("DELETE FROM Transactions WHERE Transaction_ID = %s", (record_id,))

    conn.commit()
    cursor.close()
    conn.close()

def menu():
    while True:
        print("\nLibrary Management System Menu")
        print("1. Insert Data")
        print("2. View Data")
        print("3. Update Data")
        print("4. Delete Data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            table = input("Enter table name (Publishers, Books, Users, Transactions): ")
            insert_data(table)
        elif choice == '2':
            table = input("Enter table name or view (Publishers, Books, Users, Transactions, ActiveTransactions, AvailableBooks): ")
            view_data(table)
        elif choice == '3':
            table = input("Enter table name (Books, Users, Transactions): ")
            update_data(table)
        elif choice == '4':
            table = input("Enter table name (Publishers, Books, Users, Transactions): ")
            delete_data(table)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
