import json
import os

# Load the spells data from spells.json
input_file = "/home/faye/dev/fayeleigh.com/laptop/faye-leigh-git.github.io/dnd/data/spells.json"
output_dir = "/home/faye/dev/fayeleigh.com/laptop/faye-leigh-git.github.io/dnd/spells"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the JSON data
with open(input_file, "r", encoding="utf-8") as file:
    spells = json.load(file)

# Template for the HTML page
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{spell_name}</title>
    <link rel="stylesheet" href="../../assets/css/styles.css">
</head>
<body>
    <header>
        <h1>{spell_name}</h1>
    </header>
    <main>
        <section>
            <h2>Spell Details</h2>
            <p><strong>Level:</strong> {level}</p>
            <p><strong>School:</strong> {school}</p>
            <p><strong>Casting Time:</strong> {cast_time}</p>
            <p><strong>Ritual:</strong> {ritual}</p>
            <p><strong>Range:</strong> {range}</p>
            <p><strong>Components:</strong> {components}</p>
            <p><strong>Materials:</strong> {materials}</p>
            <p><strong>Duration:</strong> {duration}</p>
            <p><strong>Concentration:</strong> {concentration}</p>
        </section>
        <section>
            <h2>Description</h2>
            <p>{description}</p>
        </section>
        <section>
            <p><strong>Classes:</strong> {classes}</p>
            <p><strong>Source:</strong> {source}</p>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 Faye Leigh. All rights reserved.</p>
    </footer>
</body>
</html>
"""

# Generate an HTML file for each spell
for spell in spells:
    # Skip entries without a spell name
    if not spell.get("spell"):
        continue

    # Prepare the data for the HTML template
    spell_name = spell["spell"]
    level = spell.get("level", "Unknown")
    school = spell.get("school", "Unknown")
    cast_time = spell.get("cast-time", "Unknown")
    range_ = spell.get("range", "Unknown")
    components = spell.get("components", "Unknown")
    materials = spell.get("materials", "None")
    duration = spell.get("duration", "Unknown")
    ritual = "Yes" if spell.get("ritual", False) else "No"
    concentration = "Yes" if spell.get("concentration", False) else "No"
    classes = ", ".join(spell.get("class", []))
    source = spell.get("source", "Unknown")
    description = spell.get("description", "No description available")

    # Format the HTML content
    html_content = html_template.format(
        spell_name=spell_name,
        level=level,
        school=school,
        cast_time=cast_time,
        range=range_,
        components=components,
        materials=materials,
        duration=duration,
        ritual=ritual,
        concentration=concentration,
        classes=classes,
        source=source,
        description=description
    )

    # Create a filename-safe version of the spell name
    filename = f"{spell_name.lower().replace(' ', '-').replace('/', '-')}.html"

    # Write the HTML file
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(html_content)

    print(f"Generated: {output_path}")

print("All spell pages have been generated.")