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


def create_link(brain, node):
    brain_path = pathlib.Path(f"../storage/{brain}")
    node_path = brain_path / f"{node}.json"
    nodes = [f.name for f in brain_path.iterdir() if f.is_file()]

    node_data = {}
    try:
        with open(node_path, "r") as file:
            node_data = json.load(file)
    except FileNotFoundError:
        print("File not found")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format!")
        return

    print("These are the available nodes")
    node_links = node_data.get("node_links", [])

    for i in nodes:
        print(i, end=" " * 6)
    print()

    while True:
        node_to_add = input("Node name:\n").strip()
        if not node_to_add:
            break
        node_links.append(node_to_add)

    with open(node_path, "w") as file:
        json.dump(node_data, file, indent=2)
