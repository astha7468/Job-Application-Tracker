from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import json

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