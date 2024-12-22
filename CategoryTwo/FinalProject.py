from pymongo import MongoClient
import hashlib
from dotenv import load_dotenv
import os
import getpass

def hash_password(password):
    """
    Hashes the password using SHA-256 for secure storage and comparison.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def connect_to_mongodb(uri, database_name, collection_name):
    """
    Connects to MongoDB and returns the collection object.
    """
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]
    return collection


def check_credentials(collection, username, password, role):
    """
    Checks if the username and password exist in the MongoDB collection.
    """
    hashed_password = hash_password(password)
    user = collection.find_one({"Username": username, "Password": hashed_password, "Role": role})
    return user is not None

def create_user(collection, username, password, role, brokerage, retirement):
    """
    Creates a new user in the MongoDB collection.
    """
    hashed_password = hash_password(password)
    user = collection.find_one({"Username": username})
    role = "user"
    new_user = {"Username": username, "Password": hashed_password, "Role": role, "Brokerage": brokerage, "Retirement": retirement}

    if user is not None:
        print("Username already exists")
    else:
        collection.insert_one(new_user)
        print("User created successfully.")
    

def read_user(collection, username):
    """
    Reads a user's information from the MongoDB collection.
    """
    user = collection.find_one({"Username": username})
    if user:
        print(f"User found: {user}")
    else:
        print("User not found.")

def update_user(collection, username, new_password):
    """
    Updates a user's password in the MongoDB collection.
    """
    hashed_password = hash_password(new_password)
    result = collection.update_one({"Username": username}, {"$set": {"Password": hashed_password}})
    if result.modified_count > 0:
        print("User password updated successfully.")
    else:
        print("User not found or password not updated.")

def delete_user(collection, username):
    """
    Deletes a user from the MongoDB collection.
    """
    result = collection.delete_one({"Username": username})
    if result.deleted_count > 0:
        print("User deleted successfully.")
    else:
        print("User not found.")


def admin_menu(collection):
    """
    Displays the admin menu and handles CRUD operations.
    """
    while True:
        print("\nAdmin Menu:")
        print("1. Create User")
        print("2. Read User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            verify_password = getpass.getpass("Re-enter password: ")
            brokerage = input("Enter the Brokerage amount: ")
            retirement = input("Enter the Retiremenet amount: ")
            if password == verify_password:
                role = input("Enter role (admin/user): ").lower()
                create_user(collection, username, password, role, brokerage, retirement)
            else:
                print("Passwords do not match")
        elif choice == "2":
            username = input("Enter username to read: ")
            read_user(collection, username)
        elif choice == "3":
            username = input("Enter username to update: ")
            new_password = input("Enter new password: ")
            update_user(collection, username, new_password)
        elif choice == "4":
            username = input("Enter username to delete: ")
            delete_user(collection, username)
        elif choice == "5":
            print("Exiting admin menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu():
    """
    Displays the user menu.
    """
    print("\nUser Menu:")
    print("1. View Profile")
    print("2. Exit")

    while True:
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Profile viewing is not implemented yet.")
        elif choice == "2":
            print("Exiting user menu.")
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    load_dotenv()
    # MongoDB connection settings
    uri = os.getenv("MONGODB_URI")  
    database_name = "CS499Final"
    collection_name = "Users"

    # Connect to the database
    collection = connect_to_mongodb(uri, database_name, collection_name)

    print("Created by Tyler Bennett")
    print("Hello! Welcome to our Investment Company")

    # Limit login attempts
    attempts = 0
    max_attempts = 3


    while attempts < max_attempts:
        # Prompt user for credentials
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        role = input("Enter role (admin/user): ").lower()
        # Check credentials
        user = check_credentials(collection, username, password, role)

        if user:
            print(f"Login successful! Welcome, {username}!")
            if role == "admin":
                admin_menu(collection)
            else:
                user_menu()
        else:
            attempts += 1
            print(f"Invalid username or password. Attempt {attempts} of {max_attempts}.")

    print("Maximum login attempts reached. Access denied.")

if __name__ == "__main__":
    main()
