import os
import aiohttp
import asyncio
import json
from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
import time

# Load the search terms from the JSON file
with open("categorized_aircraft_all.json", "r") as file:
    data = json.load(file)

# Get the list of aircraft names from the categories
categories = {
    "single_engine_aircraft": data.get("Single Engine Aircraft", []),
    "multi_engine_aircraft": data.get("Multi Engine Aircraft", []),
    "jet_aircraft": data.get("Jet", []),
}

# Bing search URL configuration
bing_url = "https://www.bing.com/images/async"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Tracking file for downloaded images
progress_file = "downloaded_images.json"

# Load the list of downloaded images
def load_downloaded_images():
    if os.path.exists(progress_file):
        with open(progress_file, "r") as file:
            return json.load(file)
    return {
        "single_engine_aircraft": {},
        "multi_engine_aircraft": {},
        "jet_aircraft": {}
    }

# Save the list of downloaded images
def save_downloaded_images(downloaded_images):
    with open(progress_file, "w") as file:
        json.dump(downloaded_images, file, indent=4)

# Ensure directory structure for saving images
def ensure_directory(base_directory, category, aircraft_name):
    directory_path = os.path.join(base_directory, category, aircraft_name.replace(" ", "_").lower())
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

# Asynchronous function to fetch image URLs
async def fetch_image_urls(search_term, session, max_results=1000):
    image_urls = []
    params = {"q": search_term, "count": 50, "first": 0, "adlt": "off", "qft": ""}
    first = 0
    max_attempts = 2

    while len(image_urls) < max_results and max_attempts > 0:
        params["first"] = first
        try:
            async with session.get(bing_url, headers=headers, params=params) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                image_elements = soup.find_all("a", class_="iusc")

                for element in image_elements:
                    m = element.get("m")
                    if m:
                        try:
                            m_data = json.loads(m)
                            image_url = m_data.get("murl")
                            if image_url and image_url not in image_urls:
                                image_urls.append(image_url)
                        except (json.JSONDecodeError, TypeError):
                            continue  # Handle any malformed JSON or missing data

                first += 100  # Move to the next page of search results
                max_attempts -= 1  # Decrease attempts to prevent infinite loop

        except Exception as e:
            print(f"Error fetching image URLs for {search_term}: {e}")
            break  # If there's a network error, stop trying

    return image_urls[:max_results]


# Asynchronous function to download images
async def download_image(url, session, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, "wb") as f:
                    f.write(await response.read())
                print(f"Downloaded {url}")
            else:
                print(f"Failed to download {url}, Status Code: {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Main function to scrape and download images
async def scrape_and_download_images():
    downloaded_images = load_downloaded_images()

    # Initialize session
    async with aiohttp.ClientSession() as session:
        for category, aircraft_names in categories.items():
            for aircraft_name in aircraft_names:
                aircraft_dir = ensure_directory("images", category, aircraft_name)
                image_urls = await fetch_image_urls(aircraft_name, session, max_results=1000)

                for i, url in enumerate(image_urls):
                    if len(downloaded_images[category].get(aircraft_name, [])) >= 1000:
                        print(f"Already downloaded 500 images for {aircraft_name}. Skipping...")
                        break

                    # Download the image
                    image_path = os.path.join(aircraft_dir, f"{aircraft_name.replace(' ', '_').lower()}_{i + 1}.jpg")
                    await download_image(url, session, image_path)

                    # Add to the downloaded images record
                    downloaded_images[category].setdefault(aircraft_name, []).append(url)

                # Save the downloaded images record
                save_downloaded_images(downloaded_images)

# Run the script
asyncio.run(scrape_and_download_images())
