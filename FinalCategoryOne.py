'''
Tyler Bennett
CS 499
Category One
'''

from multiprocessing import Value
import sys


users = {
    "admin": {"name": "admin", "password": "Temporal1", "service": 1},
    "Sarah Davis": {"name": "Sarah Davis", "password": "F2umis7uw.", "service": 2},
    "Amy Friendly": {"name": "Amy Friendly", "password": "Ivenab88!", "service": 1},
    "Johnny Smith" : {"name": "Johny Smith", "password": "Granet317", "service": 1},
    "Bob Jones": {"name": "Bob Jones", "password": "Password", "service": 2}
}


def check_user_permission_access():
    """
    Check that user is allowed access
    Security vulnerabilities identified below. Encrypt user password.
    Validate input.
    Minimum/maximum password length using alphanumerics
    """
    
    # declares max number of login attempts
    max_attempts = 3

    #loop until succcesful login or max number of attempts
    attempts = 0
    while attempts < max_attempts:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in users and users[username]["password"] == password:
            print("Login successful!")
            return True
        else:
            attempts += 1
            print(f"Invalid credentials. {max_attempts - attempts} attempts left.")
    return False


def display_info():
    print("Client's Name | Service Selected (1 = Brokerage, 2 = Retirement)")
    for username, user_info in users.items():
        service_name = "Brokerage" if user_info['service'] == 1 else "Retirement"
        print(f"{username}: {'service_name'}")

# Function to change a client's service choice
def change_customer_choice():
    try:
        # Display the client list with corresponding numbers
        print("Available clients:")
        for i, client in enumerate(users.keys(), 1):
            print(f"{i}. {client}")

        # Ask the user for a client choice (1-5)
        change_choice = int(input("\nEnter the number of the client that you wish to change (1-5): "))
        if change_choice < 1 or change_choice > len(users):
            print("Invalid client number. Please choose a number between 1 and 5.")
            return
        
        # Get the corresponding client name
        client_name = list(users.keys())[change_choice - 1]

        # Ask for a new service choice
        new_service = int(input("Please enter the client's new service choice (1 = Brokerage, 2 = Retirement): "))
        if new_service not in [1, 2]:
            print("Invalid service choice. Please select 1 for Brokerage or 2 for Retirement.")
            return
        
        # Update the client's service choice
        users[client_name]["service"] = new_service
        print(f"Client {client_name}'s service choice has been updated to {'Brokerage' if new_service == 1 else 'Retirement'}.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def main():
    print("Created by Tyler Bennett")
    print("Hello! Welcome to our Investment Company")

    # Check if user is authenticated.
    # Use a login counter to verify if > 3 attempts

    if not check_user_permission_access():
        print("Too many incorrect attempts. Exiting.")
        return
    # Gets what user wants to do
    while True:
        print("What would you like to do?")
        print("DISPLAY the client list (enter 1)")
        print("CHANGE a client's choice (enter 2)")
        print("Exit the program (enter 3)")

        try:
            answer = int(input())
            print(f"You chose {answer}")
            if answer == 1:
                display_info()
            elif answer == 2:
                change_customer_choice()
            elif answer == 3:
                print("Exiting program.")
                sys.exit(0)
            else:
                print("Invalid option. Please select 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter a valid number.")



if __name__ == "__main__":
    main()




