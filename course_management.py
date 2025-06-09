import json
import random

# File paths
USER_DATA_FILE = "user_data.json"
COURSES_FILE = "courses.json"

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

# Load courses from JSON file
def load_courses():
    try:
        with open(COURSES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Automatically assign 2 to 3 random courses to the user
def auto_assign_courses(logged_in_user):
    courses = load_courses()
    assigned_courses = random.sample(courses, k=min(3, len(courses)))  # Randomly select up to 3 courses

    # Add tasks to each assigned course
    for course in assigned_courses:
        course["tasks"] = [
            f"Complete the first module of {course['name']}",
            f"Submit the assignment for {course['name']}",
            f"Attend the Q&A session for {course['name']}",
        ]

    # Assign courses to the user
    logged_in_user["assigned_courses"] = assigned_courses
    print(f"Courses assigned to {logged_in_user['name']}:")
    for course in assigned_courses:
        print(f"- {course['name']}")

# View assigned courses and their tasks
def view_assigned_courses(logged_in_user):
    assigned_courses = logged_in_user.get("assigned_courses", [])
    if assigned_courses:
        print("\n--- Your Assigned Courses and Tasks ---")
        for course in assigned_courses:
            print(f"\nCourse: {course['name']}")
            print(f"Description: {course['description']}")
            print("Tasks:")
            for task in course.get("tasks", []):
                print(f"- {task}")
    else:
        print("You have not been assigned any courses yet.")

# User dashboard after login
def user_dashboard(logged_in_user):
    # Automatically assign courses if the user has no courses assigned
    if "assigned_courses" not in logged_in_user or not logged_in_user["assigned_courses"]:
        auto_assign_courses(logged_in_user)

    while True:
        print("\n--- User Dashboard ---")
        print(f"Welcome, {logged_in_user['name']}!")
        print("1. View Assigned Courses and Tasks")
        print("2. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # View assigned courses and tasks
            view_assigned_courses(logged_in_user)
        elif choice == "2":
            # Logout
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Main function to handle course management
def course_management(logged_in_user):
    # Load all users
    users = load_user_data()

    # Find the logged-in user in the list
    for user in users:
        if user["email"] == logged_in_user["email"]:
            # Pass the user object to the dashboard
            user_dashboard(user)
            break

    # Save updated user data
    save_user_data(users)
