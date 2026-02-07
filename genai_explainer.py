from google import genai
from dotenv import load_dotenv;
import os,asyncio;


load_dotenv()
key=os.getenv('key')
client = genai.Client(api_key=key)
def explain_medicine(med: dict) -> str:
    prompt = f"""
    Explain the following medicine in simple language for normal users.
    Do NOT give diagnosis.
    Do NOT suggest dosage.
    Always advise consulting a doctor.

    Medicine Name: {med['name']}
    Usage: {med.get('medical_usage')}
    Side Effects: {med.get('side_effects')}
    Warnings: {med.get('warnings')}
    Age Restriction: {med.get('age_restriction')}
    """


    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
    )

    return response.text