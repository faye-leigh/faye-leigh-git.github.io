import json
import os

# Load the spells data from spells.json
input_file = "unlisted/dnd/data/spells.json"
output_file = "unlisted/dnd/spells.html"

# Load the JSON data
with open(input_file, "r", encoding="utf-8") as file:
    spells = json.load(file)

# HTML template for the table page
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spells Table</title>
    <link rel="stylesheet" href="../../assets/css/styles.css">
    <style>
        th {{
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Spells Table</h1>
    </header>
    <main>
        <table id="spellsTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Spell</th>
                    <th onclick="sortTable(1)">Level</th>
                    <th onclick="sortTable(2)">School</th>
                    <th onclick="sortTable(3)">Casting Time</th>
                    <th onclick="sortTable(4)">Range</th>
                    <th onclick="sortTable(5)">Duration</th>
                    <th onclick="sortTable(6)">Ritual</th>
                    <th onclick="sortTable(7)">Concentration</th>
                    <th onclick="sortTable(8)">Classes</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </main>
    <footer>
        <p>&copy; 2025 Faye Leigh. All rights reserved.</p>
    </footer>
    <script>
        function sortTable(columnIndex) {{
            const table = document.getElementById("spellsTable");
            const rows = Array.from(table.rows).slice(1); // Exclude header row
            const isNumeric = !isNaN(rows[0].cells[columnIndex].innerText);

            rows.sort((a, b) => {{
                const cellA = a.cells[columnIndex].innerText.toLowerCase();
                const cellB = b.cells[columnIndex].innerText.toLowerCase();

                if (isNumeric) {{
                    return parseFloat(cellA) - parseFloat(cellB);
                }} else {{
                    return cellA.localeCompare(cellB);
                }}
            }});

            rows.forEach(row => table.tBodies[0].appendChild(row)); // Reorder rows
        }}
    </script>
</body>
</html>
"""

# Generate table rows for each spell
rows = ""
for spell in spells:
    if not spell.get("spell"):  # Skip invalid entries
        continue

    spell_name = spell["spell"]
    level = spell.get("level", "Unknown")
    school = spell.get("school", "Unknown")
    cast_time = spell.get("cast-time", "Unknown")
    range_ = spell.get("range", "Unknown")
    duration = spell.get("duration", "Unknown")
    ritual = "Yes" if spell.get("ritual", False) else "No"
    concentration = "Yes" if spell.get("concentration", False) else "No"
    classes = ", ".join(spell.get("class", []))

    # Create a table row
    rows += f"""
    <tr>
        <td><a href="./spells/{spell_name.lower().replace(' ', '-').replace('/', '-')}.html">{spell_name}</a></td>
        <td>{level}</td>
        <td>{school}</td>
        <td>{cast_time}</td>
        <td>{range_}</td>
        <td>{duration}</td>
        <td>{ritual}</td>
        <td>{concentration}</td>
        <td>{classes}</td>
    </tr>
    """

# Format the final HTML content
html_content = html_template.format(rows=rows)

# Write the HTML file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Sortable spells table page generated: {output_file}")