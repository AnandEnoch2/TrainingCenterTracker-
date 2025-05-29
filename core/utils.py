import requests

def get_location_name(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }
        headers = {
            "User-Agent": "YourAppName/1.0 (contact@example.com)"
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        return data.get("display_name", "Unknown Location")
    except Exception as e:
        print(f"Location lookup failed: {e}")
        return "Unknown Location"
