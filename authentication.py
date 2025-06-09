# Python

import json

# File path for user data
USER_DATA_FILE = "user_data.json"

# Load user data from JSON file
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save user data to JSON file
def save_user_data(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Register a new user
def register_user():
    print("\n--- Register New User ---")
    email = input("Enter your email: ").strip()
    name = input("Enter your name: ").strip()
    password = input("Create a password: ").strip()

    # Load existing users
    users = load_user_data()

    # Check if the email is already registered
    if any(user["email"] == email for user in users):
        print("This email is already registered. Please log in.")
        return

    # Add new user to the list
    users.append({"email": email, "name": name, "password": password})
    save_user_data(users)
    print("Registration successful! You can now log in.")

# Login an existing user
from course_management import course_management

def login_user():
    print("\n--- Login ---")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    # Load existing users
    users = load_user_data()

    # Verify user credentials
    for user in users:
        if user["email"] == email and user["password"] == password:
            print(f"Welcome back, {user['name']}!")
            course_management(user)  # Call course management after login
            return True

    # If credentials are invalid
    print("User not found. Please register and try entering the correct data.")
    return False



# Main function for authentication
def authentication_menu():
    while True:
        print("\n--- Authentication Menu ---")
        print("1. Register (New User)")
        print("2. Login (Existing User)")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            if login_user():
                break  # Exit the authentication loop after successful login
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the authentication menu
if __name__ == "__main__":
    authentication_menu()
