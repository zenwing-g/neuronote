import json
import random
import jinja2
import string
import pathlib
import re
import subprocess
from create_book import create_book
from create_check_id import create_id

# Ask the user to enter a book name.
# If the book exists, use it. Otherwise, create a new book folder.
book = input("Enter book name or create a new one:\n")
book_dir = pathlib.Path("../../storage/bag/") / book  # Path where the book is stored.

if not book_dir.exists():
    create_book(book_dir)  # Create the book if it doesn't exist.
else:
    print(book_dir)  # If it exists, just print the path.


# JSON template for a page (stored as a constant since it doesn’t change).
PAGE_TEMPLATE = """{
    "page_title": "{{ page_title }}",
    "page_id": "{{ page_id }}",
    "page_content": {{ page_content | tojson }}
}"""

# Ask the user for a page title.
page_title = input("Page Title:\n")

# Replace any characters that aren’t allowed in filenames with underscores.
sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", page_title)
page_path = book_dir / f"{sanitized_title}.json"  # The full path to the page file.


def write_page():
    """Open the page content in Neovim, allow the user to edit, and return the final content."""
    temp_file = pathlib.Path(
        f"/tmp/{sanitized_title}.md"
    )  # Temporary file for editing.

    if page_path.exists():
        # If the page already exists, load its current content.
        with page_path.open("r", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_content = existing_data.get("page_content", "")

        # Write the existing content to the temp file so the user can edit it.
        with temp_file.open("w", encoding="utf-8") as temp:
            temp.write(existing_content or "")

    # Open the temp file in Neovim for editing.
    subprocess.run(["nvim", str(temp_file)])

    if temp_file.exists():
        # Read the updated content after editing.
        with temp_file.open("r", encoding="utf-8") as file:
            content = file.read()
        temp_file.unlink()  # Delete the temp file after reading.
        return content  # Return the edited content.

    print("Error: No content was saved!")  # Just in case something goes wrong.
    return ""


# Create a dictionary containing page data (title, ID, content).
data = {"page_title": page_title, "page_id": create_id(), "page_content": write_page()}

# Render the JSON content using Jinja2 (fill in the template with actual values).
json_content = jinja2.Template(PAGE_TEMPLATE).render(data)

# Save the rendered JSON to the page file.
with page_path.open("w", encoding="utf-8") as file:
    file.write(json_content)

print(f"Page saved successfully as {page_path}")  # Confirmation message.
