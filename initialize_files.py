# Python

import json

# File paths
USER_DATA_FILE = "user_data.json"
COURSES_FILE = "courses.json"

# Initialize user data file
def initialize_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            print(f"{USER_DATA_FILE} already exists.")
    except FileNotFoundError:
        print(f"Creating {USER_DATA_FILE}...")
        with open(USER_DATA_FILE, "w") as file:
            json.dump([], file, indent=4)
        print(f"{USER_DATA_FILE} created successfully!")

# Initialize courses file
def initialize_courses():
    try:
        with open(COURSES_FILE, "r") as file:
            print(f"{COURSES_FILE} already exists.")
    except FileNotFoundError:
        print(f"Creating {COURSES_FILE}...")
        sample_courses = [
            {"id": 1, "name": "Python Basics", "description": "Learn the basics of Python programming."},
            {"id": 2, "name": "Data Structures", "description": "Understand data structures and algorithms."},
            {"id": 3, "name": "Machine Learning", "description": "Introduction to machine learning concepts."},
            {"id": 4, "name": "Soft Skills Training", "description": "Improve your communication and teamwork skills."},
            {"id": 5, "name": "Web Development", "description": "Learn how to build websites using HTML, CSS, and JavaScript."}
        ]
        with open(COURSES_FILE, "w") as file:
            json.dump(sample_courses, file, indent=4)
        print(f"{COURSES_FILE} created successfully with sample courses!")

# Main function to initialize files
if __name__ == "__main__":
    initialize_user_data()
    initialize_courses()
