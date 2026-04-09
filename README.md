mock_json_places_test was used to test calling the llm without consuming google places for testing purposes.

index.py was a refactoring of flight_app2 to be utilized and hosted in vercel

flight_app2 was the python function used to call aviationstacks api to gather flight data. It pulled an arbitrary flight but would be changed to access flight data for
the given flight number.

places_api_langchainv5 used google places api to collect restaraunts around the provided lat. and long. and utilized langchains framwork to pass that data to an llm
places_api in general was intended to provide the user with available attractions in their area 

places_api_nolangcain was used to simplify the processs by directly utilizing an api call to our llm rather than using the langchain framework
