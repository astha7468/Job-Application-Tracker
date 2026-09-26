import json

with open("applications.json","r") as file:
  applications = json.load(file)


def add_application(applications):
    
    application = {
        "company": input("enter company name: ").strip(),
        "job_role": input("enter job role: ").strip(),
        "location": input("enter location: ").strip(),
        "application_date": input("enter application date: ").strip(),
        "deadline": input("enter deadline: ").strip(),
        "status": input("enter status: ").strip(),
        "job_url": input("enter job url: ").strip(),
    }
    applications.append(application)

def update_status(applications):

    for i, application in enumerate(applications):
        print(i + 1, application["company"], "-", application["job_role"])

    choice = input("Enter application number: ")
    choice = int(choice)
    if choice < 1 or choice > len(applications):
        print("invalid application number")
        return

    index = choice - 1

    new_status = input("Enter new status: ")

    applications[index]["status"] = new_status

    print("Status updated successfully!")


def delete_application(applications):
    for i, application in enumerate(applications):
        print(i + 1, application["company"], "-", application["job_role"])

    choice = input("Enter application number to delete: ")
    choice = int(choice)

    if choice < 1 or choice > len(applications):
        print("Invalid application number. ")
        return

    index = choice - 1

    del applications[index]
    print("Application deleted successfully!")


def search_application(applications):
   company=input("enter company name to search:")

   print("Searching...")
   found = False

   for application in applications:
       if application["company"].lower()== company.lower():
           print("Company:",application["company"], "-",application["job_role"], "-",application["location"],"-",application["status"])
           found=True

   if not found:
       print("no application found.")


def filter_by_status(applications):
    print("Avaliable statuses: applied,reviewed,rejected,interview scheduled")
    status=input("enter status to filter: ")

    found=False

    for application in applications:
        if application["status"].lower()== status.lower():
            print("Company:", application["company"],
                  "-",application["job_role"],
                  "-",application["status"])
            found=True

    if not found:
        print("no application found.")






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

choice="0"

while choice !='7':
   print("\nJob Application Tracker")
   print("1. Add Application")   
   print("2. View Applications")

   print("3. Update Status")
   print("4. Delete Application")
   print("5. Search Application")
   print("6. Filter Application")
   print("7. Exit")

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
       print("Exiting the program.")

   else:
         print("Invalid choice. Please try again.")

with open("applications.json","w") as file:
    json.dump(applications, file,indent=4)











