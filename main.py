import requests
import os
import csv
from datetime import datetime, timezone


# Polygon info
api_key = "CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"
url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2022-12-01/2023-01-01?adjusted=true&sort=asc&limit=12000&apiKey=CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"

data_folder = "data"
file_name = "spy_data.csv"
file_path = os.path.join(data_folder, file_name)

# Make folder if it doesn't exist already
os.makedirs(data_folder, exist_ok=True)

def fetch_data(url,file_path):
    try:
        print("starting fetch")
        #GET request
        response = requests.get(url)
        response.raise_for_status() #get status if error
        data = response.json()

        #Get as list
        results = data.get("results", [])
        if not results:
            raise ValueError("No data found in the response!")

        #Print number of results 
        print(f"Number of results: {len(results)}")
        
        #Write to CSV file
        with open(file_path, mode="w", newline ="") as f:
            writer = csv.writer(f)
            header = ["timestamp", "Open", "High", "Low", "Close", "Volume"]
            writer.writerow(header)

            for line in results:
                row = [
                    line.get("t"),  # Timestamp
                    line.get("o"),  # Open price
                    line.get("h"),  # High price
                    line.get("l"),  # Low price
                    line.get("c"),  # Close price
                    line.get("v"),  # Volume
                ]
                writer.writerow(row)

        print("Completed")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    fetch_data(url,file_path)

if __name__ == "__main__":
    main()


now = datetime.now(timezone.utc)
