from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import json
from datetime import datetime, timedelta

app = FastAPI()

applications = []


class Application(BaseModel):
    id: int | None = None
    company: str
    job_role: str
    location: str
    application_date: str
    deadline: str
    status: str
    job_url: str


# Load existing applications
with open("applications.json", "r") as f:
    applications = json.load(f)

if isinstance(applications,dict):
    applications = [applications]



for index, application in enumerate(applications, start=1):
    if "id" not in application:
        application["id"]= index


with open("applications.json", "w") as f:
    json.dump(applications, f, indent=4)


@app.get("/")
def home():
    return {"message": "Job Application Tracker API"}


@app.get("/applications")
def get_applications():
    return applications


@app.get("/applications/search")
def search_applications(
    company: str | None = None,
    job_role: str | None = None,
    location: str | None = None,
    application_date: str | None = None,
    deadline: str | None = None,
    status: str | None = None,
    job_url: str | None = None,
    id: int | None = None
):
    results = []

    for application in applications:

        if company and company.lower() not in application["company"].lower():
            continue

        if job_role and job_role.lower() not in application["job_role"].lower():
            continue

        if location and location.lower() not in application["location"].lower():
            continue

        if application_date and application_date not in application["application_date"]:
            continue

        if deadline and deadline not in application["deadline"]:
            continue

        if status and status.lower() not in application["status"].lower():
            continue

        if job_url and job_url.lower() not in application["job_url"].lower():
            continue

        if id is not None and application["id"] != id:
            continue

        results.append(application)

    return results



@app.get("/applications/filter")
def filter_applications(status: str):
    results = []

    for application in applications:
        if application["status"].lower() == status.lower():
            results.append(application)

    return results

@app.get("/applications/deadline-reminder")
def deadline_reminder(days: int = 7):

    today = datetime.today().date()
    reminder_date = today + timedelta(days=days)

    results = []

    for application in applications:
        deadline = datetime.strptime(
            application["deadline"],
            "%Y-%m-%d"
        ).date()

        if today <= deadline <= reminder_date:
            results.append(application)

    return results


@app.get("/applications/dashboard")
def dashboard():

    total = len(applications)

    status_count = {}

    for application in applications:
        status = application["status"]

        if status in status_count:
            status_count[status] += 1
        else:
            status_count[status] = 1

    return {
        "total_applications": total,
        "status_count": status_count
    }


@app.get("/applications/sort")
def sort_by_deadline():

    sorted_applications = sorted(
        applications,
        key=lambda application: application["deadline"]
    )

    return sorted_applications




@app.get("/applications/{application_id}")
def get_application(application_id: int):

    for application in applications:
        if application["id"] == application_id:
            return application

    raise HTTPException(
        status_code=404,
        detail="Application not found"
    )


@app.put("/application/{application_id}")
def update_application(application_id: int,application_data: Application):
    for application in applications:
        if application["id"]== application_id:
            application.update(application_data.model_dump(exclude={"id"}))

            with open("application.json","w") as f:
                json.dump(applications,f,indent = 4)

            return application
    raise HTTPException(
        status_code=404,
        detail = "Application not found"
    )


@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    for application in applications:
        if application["id"]== application_id:
            applications.remove(application)

            with open("application.json", "w") as f:
                json.dump(application,f,indent=4)

            return{"message": "Application deleted successfully"}
    raise HTTPException(
        status_code=404,
        detail="Application not found"
    )

@app.post("/applications")
def add_application(application_data: Application):

    new_id = max(
        (application["id"] for application in applications),
        default=0
    ) + 1

    application_data.id = new_id

    applications.append(application_data.model_dump())

    with open("applications.json", "w") as f:
        json.dump(applications, f, indent=4)

    return application_data