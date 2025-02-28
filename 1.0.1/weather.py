import requests
from geopy.geocoders import Nominatim

# Get city the user is in
def get_city() -> str:
    try:
        response: str = requests.get("https://ipinfo.io/json")
        data: str = response.json()
        return data.get("city", "City not found")
    except requests.RequestException:
        quit()

# Get the weather from the weather code
def weathercode_decypher(weather_code: int) -> str:
    match weather_code: 
        case 0:
            return "Clear sky"
        case 1:
            return "Mainly clear"
        case 2:
            return "Partly cloudy"
        case 3:
            return "Overcast"
        case 45 | 48:
            return "Fog"
        case 51 | 52 | 53 | 54 | 55:
            return "Drizzle"
        case 61 | 62 | 63 | 64 | 65:
            return "Rain"
        case 71 | 72 | 73 | 74 | 75:
            return "Snow"
        case 80 | 81 | 82:
            return "Rain showers"
        case 95 | 96 | 97 | 98 | 99:
            return "Thunderstorms"
        case _:
            return "Clear skies"

# Class that contains all data on a day
class WeatherData():
    _temp_mean: int = 0 # Private temperature mean
    _weather_code:int = -1 # Private temperature code

    _day_offset: int = 0 # The day offset (from today; is only positive)
    _location: str = None # Current location

    # Class constructor; fetches all needed weather data when a class is instantiated
    def __init__(self, day_offset: int, location: str) -> None: # Void function
        validation_check: int = 0
        
        if type(day_offset) is int:
            if day_offset >= 0 & day_offset is not None:
                validation_check += 1
        
        if location is not None and type(location) == str:
            validation_check += 1

        if validation_check == 2:
            self._day_offset = day_offset
            self._location = location

            try:
                geolocator = Nominatim(user_agent="weather_app")
                location = geolocator.geocode(self._location)

                # URL to get data from
                URL: str = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&daily=temperature_2m_mean,weathercode&timezone=auto"

                # Execute connection to the URL
                response = requests.get(URL)
                data = response.json() # Fetch data from the URL
            
                # If data was found
                if response.status_code == 200:
                    self._temp_mean = data['daily']['temperature_2m_mean'][self._day_offset]
                    self._weather_code = data['daily']['weathercode'][self._day_offset]
                else:
                    quit() # Exit app if no internet connection or a connection error occurs
            except Exception as Exception:
                quit() # Exit app if something bad happens