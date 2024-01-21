import mysql.connector
from mysql.connector import Error
from decimal import Decimal

# Function to connect to MySQL
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="8848613225",
            database="banking_app123"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to initialize the database and tables
def initialize_database(connection):
    try:
        cursor = connection.cursor()

        # Create 'banking_app' database
        cursor.execute("CREATE DATABASE IF NOT EXISTS banking_app")
        cursor.execute("USE banking_app")

        # Create 'users' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create 'accounts' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                balance DECIMAL(10, 2) DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.commit()
        print("Database initialized successfully")

    except Error as e:
        print(f"Error: {e}")

# Function for user registration
def register_user(connection):
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        print("User registered successfully")
    except Error as e:
        print(f"Error: {e}")

# Function to create a new account
def create_account(connection):
    username = input("Enter your username: ")

    # Check if the user exists
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_result = cursor.fetchone()

    if user_result:
        user_id = user_result[0]
        initial_balance = Decimal(input("Enter initial balance: "))
        
        try:
            cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (%s, %s)", (user_id, initial_balance))
            connection.commit()
            print("Account created successfully")
        except Error as e:
            print(f"Error: {e}")
    else:
        print("User not found. Please register first.")

# Function for balance inquiry
def check_balance(connection):
    username = input("Enter your username: ")

    # Check if the user exists
    cursor = connection.cursor()
    cursor.execute("SELECT a.balance FROM accounts a JOIN users u ON a.user_id = u.id WHERE u.username = %s", (username,))
    balance_result = cursor.fetchone()

    if balance_result:
        balance = balance_result[0]
        print(f"Your current balance is: {balance}")
    else:
        print("User not found. Please create an account first.")

# Function for funds transfer
def transfer_funds(connection):
    sender_username = input("Enter your username: ")

    # Check if the sender exists
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (sender_username,))
    sender_result = cursor.fetchone()

    if sender_result:
        sender_id = sender_result[0]

        recipient_username = input("Enter recipient's username: ")
        cursor.execute("SELECT id FROM users WHERE username = %s", (recipient_username,))
        recipient_result = cursor.fetchone()

        if recipient_result:
            recipient_id = recipient_result[0]
            amount = Decimal(input("Enter the amount to transfer: "))

            # Check if the sender has sufficient funds
            cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (sender_id,))
            sender_balance = cursor.fetchone()[0]

            if sender_balance >= amount:
                try:
                    # Perform the transfer
                    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE user_id = %s", (amount, sender_id))
                    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE user_id = %s", (amount, recipient_id))
                    connection.commit()
                    print("Funds transferred successfully")
                except Error as e:
                    print(f"Error: {e}")
            else:
                print("Insufficient funds")
        else:
            print("Recipient not found.")
    else:
        print("Sender not found. Please create an account first.")

# Main function
def main():
    connection = connect_to_mysql()
    if connection:
        initialize_database(connection)

        while True:
            print("\n=== Banking Application Menu ===")
            print("1. Register User")
            print("2. Create Account")
            print("3. Check Balance")
            print("4. Transfer Funds")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                register_user(connection)
            elif choice == "2":
                create_account(connection)
            elif choice == "3":
                check_balance(connection)
            elif choice == "4":
                transfer_funds(connection)
            elif choice == "5":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

        connection.close()

if __name__ == "__main__":
    main()
