from colorama import init, Fore, Style
import jinja2
import json
import random
import string
import pathlib
import re

# Initialize colorama
init(autoreset=True)

# Color settings
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RESET = Style.RESET_ALL

# Directory creation check for the brain
brain = input(BLUE + "Give the name of brain or create a new one:\n" + RESET)
storage_path = pathlib.Path(f"../storage/{brain}")

# Check if the directory exists and ask for confirmation to overwrite if it does
if storage_path.exists() and storage_path.is_dir():
    overwrite_brain = (
        input(
            YELLOW
            + f"Brain with the name '{brain}' already exists. Do you want to overwrite it? (y/n): "
            + RESET
        )
        .strip()
        .lower()
    )
    if overwrite_brain != "y":
        print(RED + "Aborting brain directory creation." + RESET)
        exit()  # Exit if user doesn't want to overwrite
else:
    storage_path.mkdir(parents=True, exist_ok=True)
    print(YELLOW + f"Directory '{brain}' created at: {storage_path}" + RESET)


# Check if an ID already exists
def check_id(file_id):
    # Create the ids.csv file if it doesn't exist
    ids_path = pathlib.Path("ids.csv")
    if not ids_path.exists():
        # Create an empty file if it doesn't exist
        ids_path.touch()

    # Check if the ID exists in the CSV file
    with ids_path.open("r", encoding="utf-8") as file:
        file_ids = {line.strip() for line in file}

    return file_id in file_ids


# Generate a unique 6-character ID
def create_id():
    characters = string.ascii_lowercase + string.digits

    while True:
        new_id = "".join(random.choices(characters, k=6))
        if not check_id(new_id):
            # Store the new ID in ids.csv
            with pathlib.Path("ids.csv").open("a", encoding="utf-8") as file:
                file.write(new_id + "\n")
            return new_id


# Jinja2 JSON template for the node
node_template = """{
    "node_title": "{{ node_title }}",
    "node_id": "{{ node_id }}",
    "node_content": {{ node_content | tojson }}
}"""

# User input for the node title, ID, and content
node_title = input(YELLOW + "Node Title:\n" + RESET)
data = {
    "node_title": node_title,
    "node_id": create_id(),
    "node_content": input(YELLOW + "Give the content in Markdown format:\n" + RESET),
}

# Sanitize the node_title to make it a valid filename
safe_title = re.sub(
    r'[\\/*?:"<>|]', "_", node_title
)  # Replace invalid characters with "_"
file_name = f"../storage/{brain}/{safe_title}.json"

# Check if the file already exists and ask for confirmation to overwrite it
if pathlib.Path(file_name).exists():
    overwrite_file = (
        input(
            YELLOW
            + f"Node with the name '{node_title}' already exists. Do you want to overwrite it? (y/n): "
            + RESET
        )
        .strip()
        .lower()
    )
    if overwrite_file != "y":
        print(RED + "Aborting file save operation." + RESET)
        exit()  # Exit if user doesn't want to overwrite

# Render the template with user data
template = jinja2.Template(node_template)
json_content = template.render(data)

# Save the formatted JSON to a file
with open(file_name, "w", encoding="utf-8") as file:
    file.write(json_content)

print(GREEN + f"Node saved successfully as {file_name}" + RESET)
