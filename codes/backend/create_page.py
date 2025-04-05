import json
import string
import jinja2
import pathlib
import re
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

# JSON template for a page (fixed syntax)
PAGE_TEMPLATE = """{
    "page_title": "{{ page_title }}",
    "page_id": "{{ page_id }}",
    "page_content": {{ page_content | tojson }},
    "page_location": {"x": {{ page_location.x }}, "y": {{ page_location.y }}},
    "page_style": {
        "color": "{{ page_style.color }}",                     // Text color
        "font_size": "{{ page_style.font_size }}",             // Size of the text
        "font_family": "{{ page_style.font_family }}",         // Font family (e.g., Arial, Courier)
        "font_weight": "{{ page_style.font_weight }}",         // Boldness (normal, bold, 100–900)
        "font_style": "{{ page_style.font_style }}",           // Normal, italic, or oblique
        "text_decoration": "{{ page_style.text_decoration }}", // Underline, line-through, etc.
        
        "padding": "{{ page_style.padding }}",                 // Space inside the label around text
        "border": "{{ page_style.border }}",                   // Complete border declaration
        "border_radius": "{{ page_style.border_radius }}",     // Rounded corners
        "border_style": "{{ page_style.border_style }}",       // Border type (solid, dashed, etc.)
        "border_width": "{{ page_style.border_width }}",       // Border thickness
        "border_color": "{{ page_style.border_color }}",       // Border color
        
        "background_color": "{{ page_style.background_color }}" // Background fill color
    }
}"""

# Ask the user for a page title.
page_title = input("Page Title:\n")

# Replace any characters that aren’t allowed in filenames with underscores.
sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", page_title)
page_path = book_dir / f"{sanitized_title}.json"  # The full path to the page file.


def get_multiline_input():
    """Read multiline input from the terminal until 'EOF' is entered."""
    print("Enter content (type 'EOF' on a new line to finish):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "EOF":
            break
        lines.append(line)
    return "\n".join(lines)


def get_page_location():
    """Get the page's coordinates from user input."""
    x_coordinate = int(input("X: ")) * 50
    y_coordinate = int(input("Y: ")) * 50
    return {"x": x_coordinate, "y": y_coordinate}  # Return as a dictionary


def get_page_style(
    color: str = "white",
    font_size: int = 14,
    font_family: str = "Arial",
    font_weight: int = 400,
    font_style: str = "normal",
    text_decoration: str = "none",
    padding: int = 7,
    border: str = "1px solid white",
    border_radius: int = 10,
    border_style: str = "solid",
    border_width: int = 2,
    border_color: str = "white",
    background_color: str = "black",
):
    return {
        "color": color,
        "font_size": font_size,
        "font_family": font_family,
        "font_weight": font_weight,
        "font_style": font_style,
        "text_decoration": text_decoration,
        "padding": padding,
        "border": border,
        "border_radius": border_radius,
        "border_style": border_style,
        "border_width": border_width,
        "border_color": border_color,
        "background_color": background_color,
    }


# Get page location
page_location = get_page_location()

# Get page style
page_style = get_page_style()

# Create a dictionary containing page data (title, ID, content, location, style)
data = {
    "page_title": page_title,
    "page_id": create_id(),
    "page_content": get_multiline_input(),
    "page_location": page_location,
    "page_style": page_style,
}

# Render the JSON content using Jinja2 (fill in the template with actual values).
json_content = jinja2.Template(PAGE_TEMPLATE).render(data)

# Save the rendered JSON to the page file.
with page_path.open("w", encoding="utf-8") as file:
    file.write(json_content)

print(f"Page saved successfully as {page_path}")
