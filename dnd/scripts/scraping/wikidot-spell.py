import requests
from bs4 import BeautifulSoup
import json

# Define the URL to scrape
url = "https://dnd5e.wikidot.com/spell:catapult"  # Replace with the actual URL

# Define the path to the JSON file
json_file_path = "dnd/data/spells.json"

def scrape_spell_data(url):
    """Scrape spell data from the given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    spells = []

    try:
        # Extract spell details based on the provided HTML structure
        spell_name = soup.find("div", class_="page-title page-header").text.strip()
        details = soup.find("div", id="page-content").find_all("p")

        # Parse spell details
        source = details[0].text.replace("Source: ", "").strip()
        level_school = details[1].text.strip()
        casting_time = details[2].find("strong", text="Casting Time:").next_sibling.strip()
        spell_range = details[2].find("strong", text="Range:").next_sibling.strip()
        components = details[2].find("strong", text="Components:").next_sibling.strip()
        duration = details[2].find("strong", text="Duration:").next_sibling.strip()

        # Extract the raw HTML for the description
        description_html = "".join(str(p) for p in details[3:])

        # Extract level and school
        level, school = level_school.split("-level ")
        level = level.strip()[0]  # Get the level number
        school = school.strip().capitalize()  # Capitalize the school name

        # Extract class list from "Spell Lists" and remove it from the description
        spell_lists = soup.find("p", text=lambda t: t and "Spell Lists" in t)
        classes = []
        if spell_lists:
            classes = [a.text.strip() for a in spell_lists.find_all("a")]
            description_html = description_html.replace(str(spell_lists), "").strip()

        # Create spell dictionary
        spell = {
            "spell": spell_name,
            "level": level,
            "school": school,
            "cast-time": casting_time,
            "range": spell_range,
            "components": components,
            "duration": duration,
            "description": description_html,  # Keep HTML formatting
            "ritual": "ritual" in components.lower(),
            "concentration": "concentration" in duration.lower(),
            "class": classes,  # Save classes here
            "source": source
        }
        spells.append(spell)
    except Exception as e:
        print(f"Error parsing spell data: {e}")

    return spells

def append_to_json_file(file_path, new_data):
    """Append new data to the existing JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Append new data
    existing_data.extend(new_data)

    # Write back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=2, ensure_ascii=False)

def main():
    # Scrape spell data
    new_spells = scrape_spell_data(url)

    if new_spells:
        # Append the new spells to the JSON file
        append_to_json_file(json_file_path, new_spells)
        print(f"Successfully appended {len(new_spells)} spells to {json_file_path}")
    else:
        print("No new spells were scraped.")

if __name__ == "__main__":
    main()