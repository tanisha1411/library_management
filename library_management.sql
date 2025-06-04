create database management;
use management;
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    membership_date DATE NOT NULL,
    user_type ENUM('Student', 'Faculty', 'Staff') NOT NULL
);
CREATE TABLE Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(50)
);
CREATE TABLE Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    isbn VARCHAR(13) UNIQUE NOT NULL,
    status ENUM('Available', 'Issued') DEFAULT 'Available',
    publisher_id INT,
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    issue_date DATE NOT NULL,
    return_date DATE,
    fine DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id)
);
CREATE TABLE Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE VIEW ActiveTransactions AS
SELECT t.transaction_id, u.name AS user_name, b.title AS book_title, t.issue_date
FROM Transactions t
JOIN Users u ON t.user_id = u.user_id
JOIN Books b ON t.book_id = b.book_id
WHERE t.return_date IS NULL;

CREATE VIEW AvailableBooks AS
SELECT book_id, title, author, genre
FROM Books
WHERE status = 'Available';

DELIMITER $$
CREATE PROCEDURE IssueBook(IN p_user_id INT, IN p_book_id INT)
BEGIN
    DECLARE book_status VARCHAR(20);
    SELECT status INTO book_status FROM Books WHERE book_id = p_book_id;

    IF book_status = 'Available' THEN
        INSERT INTO Transactions (user_id, book_id, issue_date)
        VALUES (p_user_id, p_book_id, CURDATE());

        UPDATE Books
        SET status = 'Issued'
        WHERE book_id = p_book_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book is already issued.';
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE ReturnBook(IN p_transaction_id INT)
BEGIN
    DECLARE overdue_days INT;
    DECLARE fine_amount DECIMAL(10, 2);

    SELECT DATEDIFF(CURDATE(), issue_date) INTO overdue_days
    FROM Transactions WHERE transaction_id = p_transaction_id;

    IF overdue_days > 14 THEN
        SET fine_amount = (overdue_days - 14) * 5;
    ELSE
        SET fine_amount = 0;
    END IF;

    UPDATE Transactions
    SET return_date = CURDATE(), fine = fine_amount
    WHERE transaction_id = p_transaction_id;

    UPDATE Books
    SET status = 'Available'
    WHERE book_id = (SELECT book_id FROM Transactions WHERE transaction_id = p_transaction_id);
END$$
DELIMITER ;

DELIMITER //
CREATE TRIGGER PreventIssuedBookDeletion
BEFORE DELETE ON Books
FOR EACH ROW
BEGIN
    IF OLD.status = 'Issued' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete a book that is currently issued.';
    END IF;
END;

DELIMITER //
CREATE TRIGGER LogFinePayment
AFTER UPDATE ON Transactions
FOR EACH ROW
BEGIN
    IF NEW.fine > OLD.fine THEN
        INSERT INTO FineLog (transaction_id, fine_paid, payment_date)
        VALUES (NEW.transaction_id, NEW.fine, CURDATE());
    END IF;
END;

select* from Users;
select*from Transactions;
select*from Publishers;
select* from Books;






