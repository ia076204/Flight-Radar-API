import requests
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

#google places api results into into json
def get_restaurant_data(lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 1500,
        "type": "restaurant",
        "key": "AIzaSyDITioZ6RCCzVtlnwORVzM1QmI0IWJs7VQ" #Google Key
    }

    #get the json results here
    response = requests.get(url, params=params).json()

    #error check for api call
    if response.get("status") != "OK":
        return "No restaurants found."
    
    results = response.get("results", [])[:5]

    #print results
    for r in results:
        name = r.get("name", "Unknown")
        rating = r.get("rating", "N/A")
        address = r.get("vicinity", "Unknown location")
        print(f"{name} (⭐ {rating}) - {address}")

    
    #turn that JSON into a readable string for the LLM
    return "\n".join([
    f"Name: {r.get('name', 'Unknown')}, "
    f"Rating: {r.get('rating', 'N/A')}, "
    f"Address: {r.get('vicinity', 'Unknown')}"
    for r in results
]) or "No restaurants found."

# 3. llm setup
llm = ChatOpenRouter(
    model="anthropic/claude-sonnet-4.6",
    api_key="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", #OpenRouter Key
    #headers to help prevent the 401 errors seen in your screenshots
    app_url="http://localhost:3000",
    app_title="Restaurant Summary Bot"
)

# 4. THE SUMMARY LOGIC
def run_summary(lat, lng):
    # Step A: Get the JSON data (as a formatted string)
    json_info = get_restaurant_data(lat, lng)
    
    # Step B: Prepare the prompt
    prompt = ChatPromptTemplate.from_template(
        "Based on this JSON data:\n\n{restaurant_json}\n\n"
        "Provide a short summary and recommend the best place to eat dinner."
    )
    
    #The Direct Call Prompt -> LLM
    #Output of prompt goes to llm
    chain = prompt | llm
    
    return chain.invoke({"restaurant_json": json_info})

if __name__ == "__main__":
    result = run_summary(28.6024, -81.2001)
    print("\n--- Recommendation ---\n")
    print(result.content)