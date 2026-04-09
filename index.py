from http.server import BaseHTTPRequestHandler
import requests
import pandas as pd
import os

def get_latest_flights(api_key, limit=5):
    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&limit={limit}&offset=0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            return f"<div>API Error: {data['error'].get('message', 'Unknown error')}</div>"
        
        flights = data.get("data", [])
        if not flights:
            return "<div>No flights available for this query.</div>"
            
        df = pd.DataFrame([
            {
                "Flight": f.get('flight', {}).get('iata', 'N/A'),
                "Airline": f.get('airline', {}).get('name', 'N/A'),
                "From": f.get('departure', {}).get('airport', 'N/A'),
                "To": f.get('arrival', {}).get('airport', 'N/A'),
                "Scheduled Dep": f.get('departure', {}).get('scheduled', 'N/A'),
                "Actual Dep": f.get('departure', {}).get('actual', 'N/A'),
                "Status": f.get('flight_status', 'N/A')
            } for f in flights
        ])
        
        # Convert the Pandas DataFrame directly into an HTML table
        return df.to_html(index=False, border=1)
        
    except requests.exceptions.RequestException as e:
        return f"<div>Error fetching flight data: {e}</div>"

# Vercel Serverless Function Handler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set HTTP response status code to 200 (OK)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Grab the API key from Vercel Environment Variables 
        api_key = os.environ.get("AVIATION_API_KEY")
        
        # Get the HTML table
        html_table = get_latest_flights(api_key, limit=10)
        
        # Build a simple webpage
        html_page = f"""
        <html>
        <head><title>Live Flight Tracker</title></head>
        <body>
            <h1>Live Flight Tracker</h1>
            {html_table}
        </body>
        </html>
        """
        
        # Write the HTML to the browser
        self.wfile.write(html_page.encode('utf-8'))
        return
])
# Convert the Pandas DataFrame directly into an HTML table
return df.to_html(index=False, border=1)
except requests.exceptions.RequestException as e:
return f"<p>Error fetching flight data: {e}</p>"
# Vercel Serverless Function Handler
class handler(BaseHTTPRequestHandler):
def do_GET(self):
# Set HTTP response status code to 200 (OK)
self.send_response(200)
self.send_header('Content-type', 'text/html')
self.end_headers()
# Grab the API key from Vercel Environment Variables (Fallback to your key if not set)
api_key = os.environ.get("AVIATION_API_KEY")
# Get the HTML table
html_table = get_latest_flights(api_key, limit=10)
# Build a simple webpage
html_page = f"""
<html>
<head>
<title>Latest Flights</title>
<style>
body {{ font-family: sans-serif; padding: 20px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
th {{ background-color: #f2f2f2; }}
</style>
</head>
<body>
<h1>Live Flight Tracker</h1>
{html_table}
</body>
</html>
"""
# Write the HTML to the browser
self.wfile.write(html_page.encode('utf-8'))
return
