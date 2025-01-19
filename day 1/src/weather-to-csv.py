# Use this if you want to visualize using cloudwatch. It doesn't support JSON from S3
import os
import boto3
import requests
import csv
import io
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherFetcher:
    # Initialize environment
    def __init__(e):
        e.api_key = os.getenv("WEATHER_API_KEY")
        e.bucket_name = os.getenv("AWS_BUCKET_NAME")
        e.s3_client = boto3.client("s3")

    # Create the S3 bucket if it doesn't exist
    def create_bucket(e):
        '''Check if S3 bucket exists; create if not.'''
        try:
            e.s3_client.head_bucket(Bucket=e.bucket_name)
            print(f"Bucket {e.bucket_name} exists")
        except e.s3_client.exceptions.ClientError:
            print(f"Creating new bucket {e.bucket_name}")
            try:
                e.s3_client.create_bucket(Bucket=e.bucket_name)
                print(f"Successfully created bucket: {e.bucket_name}")
            except Exception as error:
                print(f"Error creating bucket: {error}")

    # Fetch weather data from OpenWeather API
    def fetch_weather(e, city):
        '''Fetch weather data from OpenWeather API.'''
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": e.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error fetching weather data: {error}")
            return None

    # Overwrite weather data in S3 CSV file
    def overwrite_to_s3(e, weather_data, city):
        '''Overwrite the weather data in the S3 CSV file.'''
        if not weather_data:
            return False

        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')  # ISO 8601 format
        file_name = f"weather-data/{city}-weather.csv"

        # Prepare CloudWatch-compatible CSV data
        new_data = {
            "Timestamp": timestamp,  # First column (A)
            "Temperature": weather_data['main']['temp'],  # Numeric value
            "FeelsLike": weather_data['main']['feels_like'],  # Numeric value
            "Humidity": weather_data['main']['humidity']  # Numeric value
        }

        try:
            # Overwrite the S3 file with fresh data
            csv_buffer = io.StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=["Timestamp", "Temperature", "FeelsLike", "Humidity"])
            
            # Write the header only once
            writer.writeheader()
            writer.writerow(new_data)  # Write the new data entry

            # Upload the new CSV content to S3
            e.s3_client.put_object(
                Bucket=e.bucket_name,
                Key=file_name,
                Body=csv_buffer.getvalue(),
                ContentType='text/csv'
            )
            print(f"Successfully overwritten the file {file_name} with new data in S3")
            return True
        except Exception as error:
            print(f"Error overwriting file: {error}")
            return False


def main():
    dashboard = WeatherFetcher()

    # Create the bucket if needed
    dashboard.create_bucket()

    # List of cities updated as per your request
    cities = ["China", "Canada", "Nigeria", "India"]

    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']

            print(f"Temperature: {temp}°C")
            print(f"Feels like: {feels_like}°C")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")

            # Overwrite data to S3 CSV file
            success = dashboard.overwrite_to_s3(weather_data, city)
            if success:
                print(f"Weather data for {city} overwritten to S3 as CloudWatch-compatible CSV!")
        else:
            print(f"Failed to fetch weather data for {city}")

if __name__ == "__main__":
    main()
