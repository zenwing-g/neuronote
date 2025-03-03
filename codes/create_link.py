from colorama import init, Fore, Style
import json
import pathlib

init(autoreset=True)

GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
RESET = Style.RESET_ALL


book = input(f"{YELLOW}Book name:\n{RESET}")
book_path = pathlib.Path(f"../bag/{book}")

if not book_path.exists():
    create_book = (
        input(f"{YELLOW}The book '{book}' does not exist. Create it? (y/n): {RESET}")
        .strip()
        .lower()
    )
    if create_book == "y":
        book_path.mkdir(parents=True, exist_ok=True)
        print(f"{GREEN}Book '{book}' created successfully!{RESET}")
    else:
        print(f"{RED}Operation cancelled. No book created.{RESET}")
        exit(1)

files = [f.stem for f in book_path.iterdir() if f.is_file()]

if not files:
    print(f"{YELLOW}No pages available in '{book}'.{RESET}")
else:
    print(f"{YELLOW}Available pages:{RESET}")
    for i in files:
        print(i, end=" " * 6)
    print("\n")

while True:
    page1_name = input(f"{YELLOW}Page 1 name:\n{RESET}")
    if not page1_name:
        exit(1)
    if page1_name not in files:
        print(f"{RED}Name not found. Try again.{RESET}")
        continue

    page2_name = input(f"{YELLOW}Page 2 name:\n{RESET}")
    if not page2_name:
        exit(1)
    if page2_name not in files:
        print(f"{RED}Name not found. Try again.{RESET}")
        continue

    break

page1_path = book_path / f"{page1_name}.json"
page2_path = book_path / f"{page2_name}.json"

if not page1_path.exists() or not page2_path.exists():
    print(f"{RED}Error: One or both pages do not exist.{RESET}")
    exit(1)

with open(page1_path, "r", encoding="utf-8") as file:
    page1_data = json.load(file)

with open(page2_path, "r", encoding="utf-8") as file:
    page2_data = json.load(file)


def create_link_with_name(page1_data, page2_data):
    link_id = str(page1_data["page_id"]) + str(page2_data["page_id"])
    link_style = "default"
    with open("links.csv", "a", encoding="utf-8") as file:
        file.write(f"{link_id}-{link_style}\n")


create_link_with_name(page1_data, page2_data)
