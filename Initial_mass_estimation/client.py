from dotenv import load_dotenv
from pathlib import Path
from supabase import create_client, Client
import os
#This code will bring the env file to this file
#I had to do this gymnastics as the .env file is in the project root and not in this folder
current_file = Path(__file__).resolve()
parent_directory = current_file.parent.parent
env_path = parent_directory / ".env"
load_dotenv(dotenv_path=env_path)

#This function creates the supabase client, we need the client in order to use the data API
def build_client():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    client: Client = create_client(url, key)
    return client
#This function gets data from our db and returns a list of dictionaries - 1 for each row
def fetch_data(client):
    response = (
    client.table("aircraft")
    .select("empty_mass_kg")
    .execute()
    )
    return response.data
    