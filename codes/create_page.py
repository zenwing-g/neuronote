from colorama import init, Fore, Style  # black red green yellow blue magenta cyan white
import jinja2
import json
import random
import string
import pathlib
import re
import subprocess

# Initialize colorama
init(autoreset=True)

# Color settings
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
RESET = Style.RESET_ALL

# Book creation check
book = input(BLUE + "Enter book name or create a new one:\n" + RESET)
book_path = pathlib.Path(f"../bag/{book}")

# Check if the book exists
if book_path.exists() and book_path.is_dir():
    print(YELLOW + f"{book_path}" + RESET)
else:
    book_path.mkdir(parents=True, exist_ok=True)
    print(CYAN + f"{book_path} [New]" + RESET)


# Check if an ID already exists
def check_id(page_id):
    ids_path = pathlib.Path("ids.csv")
    if not ids_path.exists():
        ids_path.touch()

    with ids_path.open("r", encoding="utf-8") as file:
        page_ids = {line.strip() for line in file}

    return page_id in page_ids


# Generate a unique 6-character ID
def create_id():
    characters = string.ascii_lowercase + string.digits

    while True:
        new_id = "".join(random.choices(characters, k=6))
        if not check_id(new_id):
            with pathlib.Path("ids.csv").open("a", encoding="utf-8") as file:
                file.write(new_id + "\n")
            return new_id


# Jinja2 JSON template for the page
page_template = """{
    "page_title": "{{ page_title }}",
    "page_id": "{{ page_id }}",
    "page_content": {{ page_content | tojson }},
    "page_links": {{ page_links | tojson }}
}"""

# User input for the page title, ID, and content
page_title = input(YELLOW + "Page Title:\n" + RESET)

# Sanitize the page_title to make it a valid filename
safe_title = re.sub(r'[\\/*?:"<>|]', "_", page_title)
page_path = pathlib.Path(f"../bag/{book}/{safe_title}.json")


def write_page():
    """Opens Neovim to edit content and returns the updated text."""
    temp_file = pathlib.Path(f"/tmp/{safe_title}.md")  # Temporary Markdown file

    # If the page already exists, load its content into the temp file
    if page_path.exists():
        with page_path.open("r", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_content = existing_data.get("page_content", "")

        if existing_content is None:
            existing_content = ""  # Ensure it is always a string

        with temp_file.open("w", encoding="utf-8") as temp:
            temp.write(existing_content)  # Pre-fill with existing content

    # Open Neovim with the temporary file
    subprocess.run(["nvim", str(temp_file)])

    # Read content after Neovim exits
    if temp_file.exists():
        with temp_file.open("r", encoding="utf-8") as file:
            content = file.read()
        temp_file.unlink()  # Remove temporary file after reading
        return content
    else:
        print(RED + "Error: No content was saved!" + RESET)
        return ""


data = {
    "page_title": page_title,
    "page_id": create_id(),
    "page_content": write_page(),  # Get existing content or new input
    "page_links": [],
}

# Render the template with user data
template = jinja2.Template(page_template)
json_content = template.render(data)

# Save the formatted JSON to a page
with page_path.open("w", encoding="utf-8") as file:
    file.write(json_content)

print(GREEN + f"Page saved successfully as {page_path}" + RESET)
