import json
from datetime import datetime


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False



with open("applications.json", "r") as file:
    applications = json.load(file)


def add_application(applications):

    application_date = input(
        "Enter application date (YYYY-MM-DD): "
    ).strip()

    deadline = input(
        "Enter deadline (YYYY-MM-DD): "
    ).strip()

    if not is_valid_date(application_date):
        print("Invalid date format. Please use YYYY-MM-DD")
        return

    if not is_valid_date(deadline):
        print("Invalid deadline format. Please use YYYY-MM-DD")
        return

    application_date_obj = datetime.strptime(
        application_date, "%Y-%m-%d"
    )

    deadline_obj = datetime.strptime(
        deadline, "%Y-%m-%d"
    )

    if deadline_obj < application_date_obj:
        print("Deadline cannot be before application date.")
        return

    application = {
        "company": input("Enter company name: ").strip(),
        "job_role": input("Enter job role: ").strip(),
        "location": input("Enter location: ").strip(),
        "application_date": application_date,
        "deadline": deadline,
        "status": input("Enter status: ").strip(),
        "job_url": input("Enter job URL: ").strip()
    }

    applications.append(application)

    print("Application added successfully!")


def update_status(applications):

    for i, application in enumerate(applications):
        print(
            i + 1,
            application["company"],
            "-",
            application["job_role"]
        )

    choice = input("Enter application number: ")
    choice = int(choice)

    if choice < 1 or choice > len(applications):
        print("Invalid application number.")
        return

    index = choice - 1

    new_status = input("Enter new status: ").strip()

    applications[index]["status"] = new_status

    print("Status updated successfully!")


def delete_application(applications):

    for i, application in enumerate(applications):
        print(
            i + 1,
            application["company"],
            "-",
            application["job_role"]
        )

    choice = input("Enter application number to delete: ")
    choice = int(choice)

    if choice < 1 or choice > len(applications):
        print("Invalid application number.")
        return

    index = choice - 1

    del applications[index]

    print("Application deleted successfully!")


def search_application(applications):

    company = input("Enter company name to search: ").strip()

    print("Searching...")

    found = False

    for application in applications:

        if application["company"].lower() == company.lower():

            print(
                "Company:", application["company"],
                "-", application["job_role"],
                "-", application["location"],
                "-", application["status"]
            )

            found = True

    if not found:
        print("No application found.")


def filter_by_status(applications):

    print(
        "Available statuses: "
        "applied, reviewed, rejected, interview scheduled"
    )

    status = input("Enter status to filter: ").strip()

    found = False

    for application in applications:

        if application["status"].lower() == status.lower():

            print(
                "Company:", application["company"],
                "-", application["job_role"],
                "-", application["location"],
                "-", application["status"]
            )

            found = True

    if not found:
        print("No application found.")


def deadline_reminder(applications):

    today = datetime.today().date()

    found = False

    for application in applications:

        deadline = datetime.strptime(
            application["deadline"],
            "%Y-%m-%d"
        ).date()

        if deadline >= today:
            days_left=(deadline-today).days

            print(
                "Company:", application["company"],
                "-", application["job_role"],
                "-", application["deadline"],
                "-",days_left,"days left"
            )

            found = True

    if not found:
        print("No upcoming deadlines.")


def view_applications(applications):

    print("\nJob Applications:")
    print("-" * 50)

    for application in applications:

        print(f"Company: {application['company']}")
        print(f"Job Role: {application['job_role']}")
        print(f"Location: {application['location']}")
        print(f"Application Date: {application['application_date']}")
        print(f"Deadline: {application['deadline']}")
        print(f"Status: {application['status']}")
        print(f"Job URL: {application['job_url']}")

        print("-" * 50)


choice = "0"

while choice != "8":

    print("\nJob Application Tracker")
    print("1. Add Application")
    print("2. View Applications")
    print("3. Update Status")
    print("4. Delete Application")
    print("5. Search Application")
    print("6. Filter Application")
    print("7. Deadline Reminder")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_application(applications)

    elif choice == "2":
        view_applications(applications)

    elif choice == "3":
        update_status(applications)

    elif choice == "4":
        delete_application(applications)

    elif choice == "5":
        search_application(applications)

    elif choice == "6":
        filter_by_status(applications)

    elif choice == "7":
        deadline_reminder(applications)

    elif choice == "8":
        print("Exiting the program.")

    else:
        print("Invalid choice. Please try again.")


with open("applications.json", "w") as file:
    json.dump(applications, file, indent=4)