import requests
import json

GOOGLE_API_KEY = ""
OPENROUTER_API_KEY = ""


#Get restaurant data (mocked)
def get_restaurant_data(lat, lng):
    print("Called get_restaurant_data (mocked)")

    #Hard-coded mock data instead of calling Google API
    restaurants = [
        {"name": "The Spicy Spoon", "rating": 4.7, "address": "123 Main St, Orlando, FL"},
        {"name": "Burger Bliss", "rating": 4.3, "address": "456 Oak Ave, Orlando, FL"},
        {"name": "Pasta Palace", "rating": 4.5, "address": "789 Pine Rd, Orlando, FL"},
        {"name": "Sushi Central", "rating": 4.8, "address": "321 Maple Blvd, Orlando, FL"},
        {"name": "Taco Town", "rating": 4.2, "address": "654 Cedar St, Orlando, FL"}
    ]

    print("Returning mock restaurant data")
    return restaurants


# Send JSON to OpenRouter (Gemini)
def summarize_with_gemini(data):
    print("Called summarize_with_gemini\n")
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
You are an assistant for a travel app.

Analyze this restaurant data and return:
1. Average rating (number)
2. One-line insight about quality
3. Best rated restaurant

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
            "model": "google/gemini-2.0-flash-001",  # replace with model id as needed
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    
    #print status of code 
    print("Status code:", response.status_code)
   # print("Response JSON:", response.text)

    result = response.json()
    return result["choices"][0]["message"]["content"]


# run everything
if __name__ == "__main__":
    lat, lng = 28.5383, -81.3792  # Example coordinates (Orlando)

    data = get_restaurant_data(lat, lng)

    if data:
        summary = summarize_with_gemini(data)
        print("\nAI Summary:\n")
        print(summary)
    else:
        print("No restaurants found.")
