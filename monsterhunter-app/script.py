import requests
import time
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/') #connect to local DB and use compass to check on database
db = client.mhw_db  # Create a database for Monster Hunter World data
collection = db.monsters  # Collection to store monster data

API_URL = "https://mhw-db.com/monsters"

def get_monster_data():
    max_retries = 5  # Max number of retries
    for attempt in range(max_retries):
        response = requests.get(API_URL)
        
        if response.status_code == 200: #success
            return response.json()
        
        elif response.status_code == 503: #service error so server sided and not client sided
            print(f"Service unavailable (503). Retrying... ({attempt+1}/{max_retries})")
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            print(f"Error fetching data: {response.status_code}") #all other API codes
            return None
    
    print("Max retries reached. Service is still unavailable.")
    return None


def validate_monster_data(data):
    if not data:
        return False
    
    # Ensure the monster data is a list and contains valid information
    if not isinstance(data, list) or len(data) == 0:
        print("Invalid data: Expected a non-empty list of monsters.")
        return False

    # Check if the first monster in the list has expected fields (name, id, etc.)
    if "name" not in data[0] or "id" not in data[0]:
        print("Invalid data structure: Missing 'name' or 'id' field.")
        return False
    
    return True


def save_to_mongo(data):
    # save each as a json schema
    for monster in data:
        monster_doc = {
            "name": monster["name"],
            "id": monster["id"],
            "type": monster["type"] if "type" in monster else "Unknown",
            "description": monster["description"] if "description" in monster else "No description available"
        }
        collection.insert_one(monster_doc)
    print("Monster data saved to MongoDB successfully!")

# Main
monster_data = get_monster_data()

if monster_data and validate_monster_data(monster_data):  
    save_to_mongo(monster_data)  
else:
    print("Data validation failed, not saving to MongoDB.")
