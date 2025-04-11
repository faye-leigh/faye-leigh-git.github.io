import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

# Base URL of the spells website
base_url = "https://www.aidedd.org/spell/"

# Fetch the main page
response = requests.get(base_url)
if response.status_code != 200:
    print("Failed to retrieve the main page.")
    exit()

# Parse the main page HTML
soup = BeautifulSoup(response.content, "html.parser")

# Gather all links that appear to lead to individual spell pages
spell_links = set()
for a in soup.find_all("a", href=True):
    full_url = urljoin(base_url, a["href"])
    if full_url.startswith(base_url) and full_url != base_url:
        spell_links.add(full_url)

spell_links = list(spell_links)
print(f"Found {len(spell_links)} spell pages.")

# Limit to the first 10 spell links (temporary for testing)
# spell_links = spell_links[:10]
# print(f"Scraping the first {len(spell_links)} spell pages.")

spells_data = []

# Iterate through each spell page and collect its data
for spell_url in spell_links:
    print(f"Scraping: {spell_url}")
    spell_response = requests.get(spell_url)
    if spell_response.status_code != 200:
        print(f"Failed to retrieve: {spell_url}")
        continue

    spell_html = spell_response.text
    spell_soup = BeautifulSoup(spell_html, "html.parser")

    # Extract spell name
    h1_tag = spell_soup.find("h1")
    spell_name = h1_tag.get_text().strip() if h1_tag else "Unknown"

    # Extract school (ecole)
    ecole_tag = spell_soup.find("div", class_="ecole")
    ecole_text = ecole_tag.get_text().strip() if ecole_tag else "Unknown"

    # Split the school string into level and school
    if " - " in ecole_text:
        level, school = ecole_text.split(" - ", 1)
        level = level.replace("level ", "").strip()  # Remove "level " prefix
        school = school.strip().capitalize()
        # Check for "(ritual)" in school and handle it
        if " (ritual)" in school.lower():
            school = school.replace(" (ritual)", "").strip()
            ritual = True
        else:
            ritual = False
    else:
        level = "Unknown"
        school = ecole_text.strip()
        ritual = False

    # Extract casting time (t)
    t_tag = spell_soup.find("div", class_="t")
    cast_time = t_tag.get_text().strip().replace("Casting Time: ", "") if t_tag else "Unknown"
    # Remove " or Ritual" from cast time and set ritual to true if applicable
    if " or Ritual" in cast_time:
        cast_time = cast_time.replace(" or Ritual", "").strip()
        ritual = True

    # Extract range (r)
    r_tag = spell_soup.find("div", class_="r")
    range_ = r_tag.get_text().strip().replace("Range: ", "") if r_tag else "Unknown"

    # Extract components (c)
    c_tag = spell_soup.find("div", class_="c")
    components = c_tag.get_text().strip().replace("Components: ", "") if c_tag else "Unknown"
    materials = ""

    # Check if components contain "M" and extract materials
    if "M" in components:
        parts = components.split("M", 1)  # Split at the first occurrence of "M"
        components = parts[0].strip() + "M"  # Keep "V", "S", and "M"
        materials = parts[1].strip()  # Everything after "M" is the material

    # Extract duration (d)
    d_tag = spell_soup.find("div", class_="d")
    duration = d_tag.get_text().strip().replace("Duration: ", "") if d_tag else "Unknown"
    # Check for "Concentration" in duration and handle it
    if "Concentration" in duration:
        duration = duration.replace("Concentration, up to ", "").strip()
        concentration = True
    else:
        concentration = False

    # Extract description
    description_tag = spell_soup.find("div", class_="description")
    if description_tag:
        description = str(description_tag).strip()
        # Remove the outer <div class="description"> tags
        description = description.replace('<div class="description">', "").replace("</div>", "").strip()
    else:
        description = "No description available"

    # Extract classes (classe)
    classe_tags = spell_soup.find_all("div", class_="classe")
    classes = [tag.get_text().strip() for tag in classe_tags]

    # Append the parsed data
    spells_data.append({
        "spell": spell_name,
        "level": level,
        "school": school,
        "cast-time": cast_time,
        "range": range_,
        "components": components,
        "materials": materials,
        "duration": duration,
        "description": description,
        "ritual": ritual,
        "concentration": concentration,
        "class": classes,
        "source": "Player's Handbook 2024 pg. "
    })

    # Be polite to the server – add a short delay between requests.
    time.sleep(0.1)

# Sort the spells alphabetically by their "spell" name
spells_data = sorted(spells_data, key=lambda x: x["spell"])

# Write the collected data to a JSON file with UTF-8 encoding
output_filename = "spells.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(spells_data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(spells_data)} spells to {output_filename}.")
