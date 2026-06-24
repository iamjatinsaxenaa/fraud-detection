from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json

app = FastAPI()


# ==========================
# Pydantic Model
# ==========================

class Patient(BaseModel):

    id: Annotated[
        int,
        Field(
            ...,
            description="ID of the Patient",
            example=1
        )
    ]

    name: Annotated[
        str,
        Field(
            ...,
            description="Name of Patient"
        )
    ]

    city: Annotated[
        str,
        Field(
            ...,
            description="City where patient lives"
        )
    ]

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            lt=120,
            description="Age of Patient"
        )
    ]

    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(
            ...,
            description="Gender of Patient"
        )
    ]

    height: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Height in meters"
        )
    ]

    weight: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Weight in kilograms"
        )
    ]

    @computed_field
    @property
    def bmi(self) -> float:

        return round(
            self.weight / (self.height ** 2),
            2
        )

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"

        elif self.bmi < 25:
            return "Normal"

        elif self.bmi < 30:
            return "Overweight"

        else:
            return "Obese"

# ==========================
# Update Details
# ==========================


class PatientUpdate(BaseModel):

    name: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Updated patient name"
        )
    ]

    city: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Updated city"
        )
    ]

    age: Annotated[
        Optional[int],
        Field(
            default=None,
            gt=0,
            lt=120,
            description="Updated age"
        )
    ]

    gender: Annotated[
        Optional[Literal["Male", "Female", "Other"]],
        Field(
            default=None,
            description="Updated gender"
        )
    ]

    height: Annotated[
        Optional[float],
        Field(
            default=None,
            gt=0,
            description="Updated height"
        )
    ]

    weight: Annotated[
        Optional[float],
        Field(
            default=None,
            gt=0,
            description="Updated weight"
        )
    ]

# ==========================
# Utility Functions
# ==========================

def load_data():

    with open("patients.json", "r") as f:
        data = json.load(f)

    return data


def save_data(data):

    with open("patients.json", "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


# ==========================
# Home APIs
# ==========================

@app.get("/")
def hello():

    return {
        "message": "Hello Python World"
    }


@app.get("/about")
def about():

    return {
        "message": "Hey, this is my first API build code"
    }


# ==========================
# View All Patients
# ==========================

@app.get("/view")
def view():

    return load_data()


# ==========================
# View Patient by ID
# ==========================

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: int = Path(
        ...,
        description="ID of patient",
        example=1,
        ge=1
    )
):

    data = load_data()

    for patient in data:

        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# ==========================
# Sort Patients
# ==========================

@app.get("/sort")
def sort_patients(

    sort_by: str = Query(
        ...,
        description="Sort by height, weight or bmi"
    ),

    order: str = Query(
        "asc",
        description="asc or desc"
    )

):

    valid_fields = [
        "height",
        "weight",
        "bmi"
    ]

    if sort_by not in valid_fields:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    if order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="Order must be asc or desc"
        )

    data = load_data()

    reverse_order = (
        True if order == "desc"
        else False
    )

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_order
    )

    return sorted_data


# ==========================
# Create New Patient
# ==========================

@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    for p in data:

        if p["id"] == patient.id:

            raise HTTPException(
                status_code=400,
                detail="Patient already exists"
            )

    data.append(
        patient.model_dump()
    )

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully"
        }
    )
 
 # Update Api Key 
    
@app.put("/update/{patient_id}")
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate
):

    data = load_data()

    for patient in data:

        if patient["id"] == patient_id:

            update_data = (
                patient_update.model_dump(
                    exclude_unset=True
                )
            )

            patient.update(update_data)

            save_data(data)

            return {
                "message":
                "Patient updated successfully",

                "patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
    

# Delete API Key
   
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int):

    data = load_data()

    for index, patient in enumerate(data):

        if patient["id"] == patient_id:

            deleted_patient = patient

            data.pop(index)

            save_data(data)

            return {
                "message": "Patient deleted successfully",
                "patient": deleted_patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )