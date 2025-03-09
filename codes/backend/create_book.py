import pathlib

STORAGE_PATH = pathlib.Path("../../storage/bag/")


def create_book(book_path):
    book_path.mkdir(parents=True, exist_ok=True)
    print(f"{book_path} [NEW]")
