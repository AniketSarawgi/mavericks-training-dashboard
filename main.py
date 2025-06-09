import json
import os

# File paths for JSON data storage
ASSESSMENT_DATA_FILE = "assessment_data.json"
PROFILE_DATA_FILE = "profile_data.json"

# Function to initialize JSON files if they don't exist
def initialize_json_files():
    if not os.path.exists(ASSESSMENT_DATA_FILE):
        with open(ASSESSMENT_DATA_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(PROFILE_DATA_FILE):
        with open(PROFILE_DATA_FILE, 'w') as f:
            json.dump([], f)

# Function to load data from a JSON file
def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to save data to a JSON file
def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Function to display main menu
def display_menu():
    print("\n--- Reporting Agent Main Menu ---")
    print("1. View Assessment Data")
    print("2. View Profile Data")
    print("3. Generate Training Progress Report")
    print("4. Add/Update Assessment Data")
    print("5. Add/Update Profile Data")
    print("6. Exit")

# Function to view assessment data
def view_assessment_data():
    data = load_data(ASSESSMENT_DATA_FILE)
    if data:
        print("\n--- Assessment Data ---")
        for entry in data:
            print(entry)
    else:
        print("\nNo assessment data available.")

# Function to view profile data
def view_profile_data():
    data = load_data(PROFILE_DATA_FILE)
    if data:
        print("\n--- Profile Data ---")
        for entry in data:
            print(entry)
    else:
        print("\nNo profile data available.")

# Function to generate a training progress report
def generate_report():
    assessment_data = load_data(ASSESSMENT_DATA_FILE)
    profile_data = load_data(PROFILE_DATA_FILE)

    print("\n--- Training Progress Report ---")
    if not assessment_data and not profile_data:
        print("No data available to generate a report.")
        return

    print("Assessment Data:")
    for entry in assessment_data:
        print(entry)

    print("\nProfile Data:")
    for entry in profile_data:
        print(entry)

# Function to add or update assessment data
def add_update_assessment_data():
    data = load_data(ASSESSMENT_DATA_FILE)
    fresher_id = input("Enter Fresher ID: ")
    quiz_score = input("Enter Quiz Score: ")
    coding_score = input("Enter Coding Challenge Score: ")
    assignment_status = input("Enter Assignment Status (Submitted/Pending): ")
    certification_status = input("Enter Certification Status (Completed/In Progress): ")

    # Check if fresher ID already exists
    for entry in data:
        if entry['FresherID'] == fresher_id:
            entry.update({
                "QuizScore": quiz_score,
                "CodingScore": coding_score,
                "AssignmentStatus": assignment_status,
                "CertificationStatus": certification_status
            })
            break
    else:
        # Add new entry if fresher ID doesn't exist
        data.append({
            "FresherID": fresher_id,
            "QuizScore": quiz_score,
            "CodingScore": coding_score,
            "AssignmentStatus": assignment_status,
            "CertificationStatus": certification_status
        })

    save_data(ASSESSMENT_DATA_FILE, data)
    print("Assessment data updated successfully.")

# Function to add or update profile data
def add_update_profile_data():
    data = load_data(PROFILE_DATA_FILE)
    fresher_id = input("Enter Fresher ID: ")
    name = input("Enter Name: ")
    department = input("Enter Department: ")
    skill_set = input("Enter Skill Set (comma-separated): ")
    training_status = input("Enter Training Status (In Progress/Completed): ")

    # Check if fresher ID already exists
    for entry in data:
        if entry['FresherID'] == fresher_id:
            entry.update({
                "Name": name,
                "Department": department,
                "SkillSet": skill_set.split(","),
                "TrainingStatus": training_status
            })
            break
    else:
        # Add new entry if fresher ID doesn't exist
        data.append({
            "FresherID": fresher_id,
            "Name": name,
            "Department": department,
            "SkillSet": skill_set.split(","),
            "TrainingStatus": training_status
        })

    save_data(PROFILE_DATA_FILE, data)
    print("Profile data updated successfully.")

# Main function to run the CLI
def main():
    initialize_json_files()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            view_assessment_data()
        elif choice == '2':
            view_profile_data()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            add_update_assessment_data()
        elif choice == '5':
            add_update_profile_data()
        elif choice == '6':
            print("Exiting Reporting Agent. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
