import jinja2
import json
import random
import string
import pathlib
import re
import subprocess

# Define storage base path
STORAGE_PATH = pathlib.Path("../../storage")

# Ask the user for a book name and create/open its directory
book = input("Enter book name or create a new one:\n")
book_path = STORAGE_PATH / "bag" / book

if not book_path.exists():
    book_path.mkdir(parents=True, exist_ok=True)
    print(f"{book_path} [New]")
else:
    print(book_path)


def check_id(page_id):
    # Check if a given page ID already exists in ids.csv
    ids_path = STORAGE_PATH / "data" / "ids.csv"
    ids_path.touch(exist_ok=True)  # Ensure file exists

    with ids_path.open("r", encoding="utf-8") as file:
        return page_id in {line.strip() for line in file}


def create_id():
    # Generate a unique 6-character alphanumeric ID for the page
    characters = string.ascii_lowercase + string.digits

    while True:
        new_id = "".join(random.choices(characters, k=6))
        if not check_id(new_id):
            with (STORAGE_PATH / "data" / "ids.csv").open(
                "a", encoding="utf-8"
            ) as file:
                file.write(new_id + "\n")
            return new_id


# JSON template for a page
page_template = """{
    "page_title": "{{ page_title }}",
    "page_id": "{{ page_id }}",
    "page_content": {{ page_content | tojson }}
}"""

# Get page title from user input
page_title = input("Page Title:\n")

# Replace invalid filename characters with underscores
safe_title = re.sub(r'[\\/*?:"<>|]', "_", page_title)
page_path = book_path / f"{safe_title}.json"


def write_page():
    # Open the page content in Neovim and return the updated content
    temp_file = pathlib.Path(f"/tmp/{safe_title}.md")

    if page_path.exists():
        # Load existing page content if the file exists
        with page_path.open("r", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_content = existing_data.get("page_content", "")

        # Write existing content to a temporary file for editing
        with temp_file.open("w", encoding="utf-8") as temp:
            temp.write(existing_content or "")

    subprocess.run(["nvim", str(temp_file)])

    if temp_file.exists():
        # Read edited content and delete temp file
        with temp_file.open("r", encoding="utf-8") as file:
            content = file.read()
        temp_file.unlink()
        return content

    print("Error: No content was saved!")
    return ""


# Create the page data dictionary
data = {"page_title": page_title, "page_id": create_id(), "page_content": write_page()}

# Render the JSON content using Jinja2
json_content = jinja2.Template(page_template).render(data)

# Save the rendered JSON to the page file
with page_path.open("w", encoding="utf-8") as file:
    file.write(json_content)

print(f"Page saved successfully as {page_path}")
