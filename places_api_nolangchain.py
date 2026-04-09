import requests
import json

GOOGLE_API_KEY = ""
OPENROUTER_API_KEY = ""


#Get restaurant data from Google Places
def get_restaurant_data(lat, lng):
    print("Called get Restaraunt data")
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": f"{lat},{lng}",
        "radius": 1500,
        "type": "restaurant",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params).json()

    if response.get("status") != "OK":
        return None

    results = response.get("results", [])[:5]

    # Extract only useful fields
    restaurants = []
    for r in results:
        restaurants.append({
            "name": r.get("name"),
            "rating": r.get("rating"),
            "address": r.get("vicinity")
        })
    print("Returning restaraunt data")
    return restaurants


#Send JSON to OpenRouter (Gemini)
def summarize_with_gemini(data):
    print("Called summarize with gemini\n")
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
    Summarize this restaurant data.
    Include:
    - Average rating
    - Short summary

    JSON:
    {json.dumps(data, indent=2)}
    """

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.0-flash-001",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    print("Status code:", response.status_code)
    print("Response JSON:", response.text)  # raw text of response

    result = response.json()
    return result["choices"][0]["message"]["content"]


#Run everything
if __name__ == "__main__":
    lat, lng = 28.5383, -81.3792  # Example: Orlando

    data = get_restaurant_data(lat, lng)

    if data:
        summary = summarize_with_gemini(data)
        print("\nAI Summary:\n")
        print(summary)
    else:
        print("No restaurants found.")