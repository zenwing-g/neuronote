import json
import pathlib

# Prompt the user for a book name and construct its path
book = input("Book name:\n")  # Get user input for the book name
book_path = pathlib.Path(
    f"../../storage/bag/{book}"
)  # Construct the book's directory path

# Check if the book (folder) exists
if not book_path.exists():
    # Ask the user whether they want to create the book if it doesn't exist
    create_book = (
        input(f"The book '{book}' does not exist. Create it? (y/n): ").strip().lower()
    )

    if create_book == "y":
        book_path.mkdir(parents=True, exist_ok=True)  # Create the book directory
        print(f"Book '{book}' created successfully!")
    else:
        print("Operation cancelled. No book created.")
        exit(1)  # Exit if the user does not want to create the book

# Retrieve the list of available pages in the book
files = [
    f.stem for f in book_path.iterdir() if f.is_file()
]  # Get all file names (without extensions) in the book directory

# If no pages exist, inform the user; otherwise, display available pages
if not files:
    print(f"No pages available in '{book}'.")
else:
    print("Available pages:")
    print("      ".join(files))  # Print all page names in a single line with spacing
    print("\n")

# Ask the user to input two page names and ensure they exist
while True:
    page1_name = input("Page 1 name:\n").strip()  # Get first page name
    if not page1_name:  # If input is empty, exit the program
        exit(1)
    if page1_name not in files:  # Check if the page exists in the book
        print("Name not found. Try again.")  # If not found, prompt again
        continue

    page2_name = input("Page 2 name:\n").strip()  # Get second page name
    if not page2_name:  # If input is empty, exit the program
        exit(1)
    if page2_name not in files:  # Check if the second page exists
        print("Name not found. Try again.")  # If not found, prompt again
        continue

    break  # Exit the loop once both valid pages are selected

# Construct full file paths for the selected pages
page1_path = book_path / f"{page1_name}.json"
page2_path = book_path / f"{page2_name}.json"

# Ensure that the selected page files actually exist before proceeding
if not page1_path.exists() or not page2_path.exists():
    print("Error: One or both pages do not exist.")
    exit(1)  # Exit the program if any selected page file is missing

# Load the content of the selected JSON page files
with open(page1_path, "r", encoding="utf-8") as file:
    page1_data = json.load(file)  # Read and parse JSON data for page 1

with open(page2_path, "r", encoding="utf-8") as file:
    page2_data = json.load(file)  # Read and parse JSON data for page 2


# Function to create a link between two pages
def create_link_with_name(page1_data, page2_data, link_style="default"):
    """
    Creates a unique link between two pages and stores it in links.csv.
    If the link already exists, it does not add a duplicate.
    """
    # Construct a unique link ID using both page IDs and the link style
    link_id = f"{page1_data['page_id']}-{page2_data['page_id']}-{link_style}"
    links_file = book_path / "links.csv"  # Define the path to links.csv

    # Check if links.csv exists and read existing links
    if links_file.exists():
        with open(links_file, "r", encoding="utf-8") as file:
            existing_links = {
                line.strip() for line in file
            }  # Load existing links into a set for fast lookup

        if link_id in existing_links:  # Check if the link already exists
            print("Link already exists")
            return  # Exit the function without writing a duplicate

    # Append the new link to links.csv
    with open(links_file, "a", encoding="utf-8") as file:
        file.write(f"{link_id}\n")  # Write the new link ID to the file

    print(f"Link {link_id} created")  # Confirm link creation


# Prompt the user for a link style and create the link
link_style = input("LinkStyle: ")
create_link_with_name(page1_data, page2_data, link_style)
