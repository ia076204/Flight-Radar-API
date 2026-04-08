import requests 
import pandas as pd

API_KEY = "7148fd451b829e2c3b71eeb52df6017c"
URL = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=1&offset=0"

#try api call
try: 
    response = requests.get(URL)
    response.raise_for_status() #Will raise an HTTPError if status !=200
    data = response.json()

    #check for api level errors
    if "error" in data:
        print("API Error:", data["error"].get("message", "Unknown error"))
    
    #check for no flight data
    else:
        
        flights = data.get("data", [])

        #Error check for available flight
        if not flights:
            print("No flights available for this query.")
        
        #process and print flight info
        else:
            df = pd.DataFrame([
            {
                #JSON flight table, handle errors with 'N/A'
                "Flight": f.get('flight', {}).get('iata', 'N/A'),
                "Airline": f.get('airline', {}).get('name', 'N/A'),
                "From": f.get('departure', {}).get('airport', 'N/A'),
                "To": f.get('arrival', {}).get('airport', 'N/A'),
                "Scheduled Dep": f.get('departure', {}).get('scheduled', 'N/A'),
                "Actual Dep": f.get('departure', {}).get('actual', 'N/A'),
                "Scheduled Arr": f.get('arrival', {}).get('scheduled', 'N/A'),
                "Actual Arr": f.get('arrival', {}).get('actual', 'N/A'),
                "Status": f.get('flight_status', 'N/A')
            }
            for f in flights
        ])
        #print the table
        print("\nLatest Flights:\n")
        print(df)

#Handle request errors, store in e variable
except requests.exceptions.RequestException as e:
    print("Error fetching flight data", e)
    exit() #stop further processing
