import pathlib

STORAGE_PATH = pathlib.Path("../../storage/bag/")


def create_book(book_path):
    book_path.mkdir(parents=True, exist_ok=True)
    print(f"{book_path} [NEW]")

    # Create links.csv inside the book_path
    links_file = book_path / "links.csv"
    links_file.touch(exist_ok=True)
    print(f"{links_file} [NEW]")
