import requests
import os
import csv
import pandas as pd
from datetime import datetime
from calendar import monthrange

# Polygon info
api_key = "CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"
url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/2024-11-02/2024-11-26?adjusted=true&sort=asc&limit=50000&apiKey=CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"

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
        with open(file_path, mode="a", newline ="") as f:
            writer = csv.writer(f)
            # header = ["timestamp", "Open", "High", "Low", "Close", "Volume"]
            # writer.writerow(header)

            for line in results:
                row = [
                    pd.to_datetime(line.get("t"), unit="ms").tz_localize("UTC").tz_convert("US/Eastern"),  # Timestamp with pandas conversion from Unix to UTC to Eastern
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

#FUTURE FUNCTIONALITY FOR ACCOMMMODATING 5 REQUESTS PER MINUTE 
def generate_urls(start_date, end_date): #Returns list of URLs

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    out_urls = []

    while current_date <= end_date:
        year, month = current_date.year, current_date.month
        last_day = monthrange(year, month)[1]  # Get the number of days in the month
        start_of_month = current_date.strftime("%Y-%m-%d")
        end_of_month = current_date.replace(day=last_day).strftime("%Y-%m-%d")

        url = f"https://api.polygon.io/v2/aggs/ticker/SPY/range/1/minute/{start_of_month}/{end_of_month}?adjusted=true&sort=asc&limit=50000&apiKey=CP7pXlsPyynAOZbpAqB8OX98ANuOG4Os"
        out_urls.append(url)

        #update for next loop
        if month == 12:  # Handle year rollover
            current_date = current_date.replace(year=year + 1, month=1, day=1)
        else:
            current_date = current_date.replace(month=month + 1, day=1)       

    return out_urls

def main():
    fetch_data(url,file_path)

if __name__ == "__main__":
    main()
