import json
import pathlib

# Ask for the book name and check if it exists
book = input("Book name:\n")
book_path = pathlib.Path(f"../bag/{book}")

if not book_path.exists():
    create_book = (
        input(f"The book '{book}' does not exist. Create it? (y/n): ").strip().lower()
    )
    if create_book == "y":
        book_path.mkdir(parents=True, exist_ok=True)
        print(f"Book '{book}' created successfully!")
    else:
        print("Operation cancelled. No book created.")
        exit(1)

# Get the list of available pages in the book
files = [f.stem for f in book_path.iterdir() if f.is_file()]

if not files:
    print(f"No pages available in '{book}'.")
else:
    print("Available pages:")
    print("      ".join(files))  # Display pages in a single line with spacing
    print("\n")

# Prompt the user for two page names and ensure they exist
while True:
    page1_name = input("Page 1 name:\n").strip()
    if not page1_name:
        exit(1)
    if page1_name not in files:
        print("Name not found. Try again.")
        continue

    page2_name = input("Page 2 name:\n").strip()
    if not page2_name:
        exit(1)
    if page2_name not in files:
        print("Name not found. Try again.")
        continue

    break  # Exit the loop once valid pages are selected

# Construct file paths for the selected pages
page1_path = book_path / f"{page1_name}.json"
page2_path = book_path / f"{page2_name}.json"

# Ensure the selected pages exist
if not page1_path.exists() or not page2_path.exists():
    print("Error: One or both pages do not exist.")
    exit(1)

# Load page data from JSON files
with open(page1_path, "r", encoding="utf-8") as file:
    page1_data = json.load(file)

with open(page2_path, "r", encoding="utf-8") as file:
    page2_data = json.load(file)


def create_link_with_name(page1_data, page2_data):
    # Create a unique link ID using both page IDs and assign a default style
    link_id = str(page1_data["page_id"]) + str(page2_data["page_id"])
    link_style = "default"

    # Append the new link to links.csv
    with open("links.csv", "a", encoding="utf-8") as file:
        file.write(f"{link_id}-{link_style}\n")


# Create a link between the selected pages
create_link_with_name(page1_data, page2_data)
