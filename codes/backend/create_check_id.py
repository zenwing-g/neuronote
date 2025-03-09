import pathlib
import random
import string


def check_id(page_id):
    """Check if a given page ID already exists in ids.csv (to avoid duplicates)."""
    ids_file = pathlib.Path("../../storage/data/ids.csv")  # Path to the IDs list.

    ids_file.touch(exist_ok=True)  # Ensure the file exists before reading.

    # Read all IDs from the file and check if the given ID is already in there.
    with ids_file.open("r", encoding="utf-8") as file:
        return page_id in {line.strip() for line in file}


def create_id():
    """Generate a unique 6-character alphanumeric ID for the page."""
    characters = string.ascii_lowercase + string.digits  # Allowed characters in the ID.

    while True:
        new_id = "".join(
            random.choices(characters, k=6)
        )  # Generate a random 6-char ID.

        if not check_id(new_id):  # Ensure the ID is unique before using it.
            with pathlib.Path("../../storage/data/ids.csv").open(
                "a", encoding="utf-8"
            ) as file:
                file.write(new_id + "\n")  # Save the new ID to the file.
            return new_id  # Return the generated unique ID.
