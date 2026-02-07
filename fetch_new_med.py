import httpx

async def fetch_from_internet(name: str):
    url = "https://api.fda.gov/drug/label.json"
    params = {
        "search": (
            f'openfda.generic_name:{name} OR '
            f'openfda.substance_name:{name} OR '
            f'openfda.brand_name:{name}'
        ),
        "limit": 1
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        if "results" not in data:
            return None

        drug = data["results"][0]

        return {
            "name": name,
            "medical_usage": drug.get("indications_and_usage", ["Not available"])[0],
            "side_effects": drug.get("adverse_reactions", ["Not available"])[0],
            "warnings": drug.get("warnings", ["Not available"])[0],
            "age_restriction": "Consult doctor"
        }

    except Exception as e:
        print("External API error:", e)
        return None




# import requests;

# def fetch_from_internet(name: str):
#     url = "https://api.fda.gov/drug/label.json"
#     params = {
#         "search": f"openfda.brand_name:{name}",
#         "limit": 1
#     }

#     try:
#         response = requests.get(url, params=params, timeout=5)

#         if response.status_code != 200:
#             return None

#         data = response.json()

#         if "results" not in data:
#             return None

#         drug = data["results"][0]

#         return {
#             "name": name,
#             "medical_usage": drug.get("indications_and_usage", ["Not available"])[0],
#             "side_effects": drug.get("adverse_reactions", ["Not available"])[0],
#             "warnings": drug.get("warnings", ["Not available"])[0],
#             "age_restriction": "Consult doctor"
#         }

#     except Exception as e:
#         print("External API error:", e)
#         return None
