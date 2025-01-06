import os
import boto3
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# mount the .env environment
load_dotenv()

class WeatherFetcher:
    # function to initialize the environment
    def __init__(e):
        e.api_key = os.getenv("WEATHER_API_KEY")
        e.bucket_name = os.getenv("AWS_BUCKET_NAME")
        e.s3_client = boto3.client("s3")

    # Fuction to Create bucket
    def create_bucket(e):
        '''Check if s3 bucket exist'''
        try:
            e.s3_client.head_bucket(Bucket=e.bucket_name)
            print(f"Bucket {e.bucket_name} exists")
        except e.s3_client.exceptions.ClientError as ex:
            print(f"Creating new bucket {e.bucket_name}")
        # Now create the bucket using the Create command
        try:
            e.s3_client.create_bucket(Bucket=e.bucket_name)
            print(f"Successfully Created new Bucket: {e.bucket_name}")
        except Exception as error:
            print(f"Error creating bucket: {error}")
    
    # API TO FETCH THE WEATHER
    def fetch_weather(e, city):
        '''Fetch weather from openweather api'''
        base_url=  "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q" : city,
            "appid" : e.api_key,
            "units" : "metric"
        }
        try:
            # send a get request
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Error fetching weather data: {error}")
            return None
        
    # save response to s3
    def save_to_s3(e, weather_data, city):
        '''save data to s3'''
        if not weather_data:
            return False
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data['timestamp'] = timestamp
            e.s3_client.put_object(
                Bucket=e.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as error:
            print(f"Error saving to S3: {error}")
            return False
def main():
    dashboard = WeatherFetcher()
    
    # Create bucket if needed
    dashboard.create_bucket()
    
    cities = ["Somalia", "Ghana", "Nigeria", "Kenya"]
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°F")
            print(f"Feels like: {feels_like}°F")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save to S3
            success = dashboard.save_to_s3(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather data for {city}")

if __name__ == "__main__":
    main()
