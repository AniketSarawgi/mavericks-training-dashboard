from profile_manager import ProfileManager

def menu():
    print("""
[1] Create Fresher Profile
[2] Update Assessment Score
[3] Add Certification
[4] Update Learning Progress
[5] View Profile
[0] Exit
""")

pm = ProfileManager()

while True:
    menu()
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        fid = input("Enter Fresher ID: ")
        name = input("Enter Name: ")
        pm.create_profile(fid, name)
    elif choice == "2":
        fid = input("Enter Fresher ID: ")
        atype = input("Assessment Type (e.g., Quiz1, Coding): ")
        score = input("Enter Score: ")
        pm.update_assessment(fid, atype, score)
    elif choice == "3":
        fid = input("Enter Fresher ID: ")
        cname = input("Certification Name: ")
        pm.update_certification(fid, cname)
    elif choice == "4":
        fid = input("Enter Fresher ID: ")
        topic = input("Topic (e.g., Git, Python): ")
        status = input("Status (Not Started / In Progress / Completed): ")
        pm.update_learning_progress(fid, topic, status)
    elif choice == "5":
        fid = input("Enter Fresher ID to view: ")
        pm.view_profile(fid)
    elif choice == "0":
        print("Exiting Profile Agent.")
        break
    else:
        print("Invalid choice. Try again.")
