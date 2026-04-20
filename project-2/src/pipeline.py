from typing import Dict
import requests
import pandas as pd

API_URL = "https://api.open-meteo.com/v1/forecast"
LOCATIONS = [
    {"name": "Jacksonville", "latitude": 30.3322, "longitude": -81.6556},           #hard coded the longitude and latitude for the cities
    {"name": "Miami", "latitude": 25.7743, "longitude": -80.1937},
    {"name": "Tampa", "latitude": 27.9475, "longitude": -82.4584},
    {"name": "Orlando", "latitude": 28.5383, "longitude": -81.3792},
    {"name": "St. Petersburg", "latitude": 27.7709, "longitude": -82.6793},
]


def fetch_forecast_by_location(locations=LOCATIONS) -> Dict:
    """
    Call Open-Meteo for all locations in one request and return data split by city name.

    Returns a dict: location name -> { latitude, longitude, elevation, timezone,
    daily_units, daily }.
    """

    forecast_by_city = {}

    for city in locations:

        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "daily": ",".join([
                "temperature_2m_max",
                "temperature_2m_min",
                "sunrise",
                "sunset",
                "uv_index_max",
                "precipitation_probability_max",
                "rain_sum",
            ]),
            "timezone": "America/New_York",
        }

        try:
            response = requests.get(API_URL, params=params, timeout=30) #created error exception catching for response status codes
            print(f"{city['name']} Status: {response.status_code}")

            response.raise_for_status()

            data = response.json()

            forecast_by_city[city["name"]] = {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "elevation": data.get("elevation"),
                "timezone": data.get("timezone"),
                "daily_units": data.get("daily_units", {}),
                "daily": data.get("daily", {})
            }

        except requests.exceptions.Timeout:
            print("Request timed out, skipping this run.")
            raise
        except requests.exceptions.RequestException as error:
            print(f"Request error: {error}")
            raise
        except ValueError as error:
            print(f"Invalid JSON response: {error}")
            raise

    return forecast_by_city

def transform(data: Dict) -> pd.DataFrame:
    """
    Transforms data into a pandas DataFrame\n
    data: Dict of Dicts
    """
    # Currently the data is a dictionary that loosely follows the below format

    # {
    #  "city": {
    #    "daily": { main_data }
    #  },
    #  . . .
    #}

    # where all items in main_data are arrays of size 7 cooresponding to the 
    # 7 forecasted days, so index 0 is the next day, index 1 is two days later, and so on
    # to make this compatible with the DataFrame type we flatten data
    rows = []
    
    # For each city
    for city, info in data.items():
        daily = info.get("daily", {})

        # For each day in the forecast
        for i, date in enumerate(daily["time"]):
            # Add that days data to rows
            rows.append({
                "city": city,
                "date": date,
                "temp_max": daily.get("temperature_2m_max", [])[i],
                "temp_min": daily.get("temperature_2m_min", [])[i],
                "sunrise": daily.get("sunrise", [])[i],
                "sunset": daily.get("sunset", [])[i],
                "uv_index": daily.get("uv_index_max", [])[i],
                "precip_probability": daily.get("precipitation_probability_max", [])[i],
                "rain_sum": daily.get("rain_sum", [])[i],
            })

    # Rows is now populated and cooresponds to 1 forecasted day since
    # there are 5 locations and 7 forecasted days per location there
    # are 35 items in rows

    # converts rows to a dataframe
    df = pd.DataFrame(rows)

    # Drop rows if there are no city or date information
    df = df.dropna(subset=["city", "date"])

    # Ensure types are accurate
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["sunrise"] = pd.to_datetime(df["sunrise"], errors="coerce")
    df["sunset"] = pd.to_datetime(df["sunset"], errors="coerce")

    df["temp_max"] = pd.to_numeric(df["temp_max"], errors="coerce")
    df["temp_min"] = pd.to_numeric(df["temp_min"], errors="coerce")
    df["uv_index"] = pd.to_numeric(df["uv_index"], errors="coerce")
    df["precip_probability"] = pd.to_numeric(df["precip_probability"], errors="coerce")
    df["rain_sum"] = pd.to_numeric(df["rain_sum"], errors="coerce")

    return df

if __name__ == "__main__":
    try:
        city_data = fetch_forecast_by_location() # extracts data
        df = transform(city_data) 
        print(df.head(35)) # Prints the entire DataFrame
    except Exception as err:
        print(f"Error occured printing data: {err}")
    
