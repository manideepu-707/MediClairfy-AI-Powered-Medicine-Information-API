import database_model;
from database import engine;
from fastapi import FastAPI,Depends;
from database import SessionLocal;
from sqlalchemy.orm import Session;
from fetch_new_med import fetch_from_internet;
from sqlalchemy import func;
from genai_explainer import explain_medicine;
from model import Medic;

app=FastAPI()


database_model.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def getting_all(db:Session=Depends(get_db)):
    return {
  "project": "MediClairfy",
  "description": "MediClairfy is an AI-powered medical information backend that provides reliable, easy-to-understand explanations about medicines. The system first checks a local database for verified information, and if unavailable, securely fetches data from trusted external medical sources, stores it, and enriches the response using Generative AI.",
  "purpose": "To reduce unsafe self-medication by delivering clear medicine information while strongly encouraging users to consult qualified doctors.",
  "features": [
    "Medicine search with database-first approach",
    "Automatic external data fetching and caching",
    "AI-generated explanations in simple language",
    "Strict data validation and structured APIs",
    "High-performance asynchronous request handling"
  ],
  "tech_stack": {
    "backend": "FastAPI (Python)",
    "database": "MySQL with SQLAlchemy ORM",
    "validation": "Pydantic",
    "external_data": "Open medical APIs (FDA)",
    "ai_layer": "Google Gemini (Generative AI)",
    "http_client": "HTTPX (Async)"
  },
  "Files_Purpose": {
  "main": "Contains the main application logic and the home endpoint of the project",
  "requirements": "Lists all required dependencies and installation details",
  "database_model": "Defines the database table schemas using SQLAlchemy ORM",
  "database": "Handles database connection and ORM session management",
  "model": "Contains Pydantic schemas with field validations",
  "fetch_new_med": "Fetches medicine information from external medical APIs",
  "genai_explainer": "Integrates Google Generative AI to generate user-friendly medicine explanations"
  },
  "disclaimer": "This application is for educational purposes only and does not replace professional medical advice."
}




# @app.get('/get_by_name/{name}')
# def fetch_by_name(name:str,db:Session=Depends(get_db)):
#     temp=db.query(database_model.Medicine).filter(database_model.Medicine.name==name).first()
#     if temp:
#         return temp
#     else:
#         external_data=fetch_new_med.fetch_from_internet(name)

#         if not external_data:
#             return 'Data not found please consult doctor'
#         else:
#             validated_data=Medic(**external_data)
#             med=database_model.Medicine(**validated_data.model_dump())
#             db.add(med)
#             db.commit()
#             db.refresh(med)
#             return med
@app.get("/get_by_name/{name}",response_model=Medic)
async def fetch_by_name(name: str, db: Session = Depends(get_db)):

    medicine = db.query(database_model.Medicine).filter(func.lower(database_model.Medicine.name) ==name.lower()).first()

    if medicine:
        return medicine

    external_data = await fetch_from_internet(name)

    if not external_data:
        return {"message": "Data not found. Please consult doctor."}

    validated = Medic(**external_data)
    med = database_model.Medicine(**validated.model_dump())

    db.add(med)
    db.commit()
    db.refresh(med)

    return med




############################################
@app.get('/explain/{name}')
async def expl(name:str,db:Session=Depends(get_db)):
    medicine = db.query(database_model.Medicine).filter(func.lower(database_model.Medicine.name) ==name.lower()).first()

    if not medicine:
        medicine=await fetch_from_internet(name)
        if not medicine:
            return {"message": "Data not found. Please consult doctor."}
        else:
            validated = Medic(**medicine)
            med = database_model.Medicine(**validated.model_dump())
            db.add(med)
            db.commit()
            db.refresh(med)
            medicine=med
    med_dict = {
        "name": medicine.name,
        "medical_usage": medicine.medical_usage,
        "side_effects": medicine.side_effects,
        "warnings": medicine.warnings,
        "age_restriction": medicine.age_restriction
    }
    explanation =explain_medicine(med_dict)

    return {
        "medicine": medicine.name,
        "explanation": explanation,
        "disclaimer": "This information is for educational purposes only. Consult a doctor."
    }
        
        
    

    

       