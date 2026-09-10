from database import Database
from library import Library
from library_item import LibraryItem, Book


def main():
    # Singleton database — same instance shared everywhere
    db = Database("database.txt")
    library = Library(db)

    # Load existing collection
    library.load_from_database()

    print("=== All items (sorted alphabetically) ===")
    for item in library.all_items():
        print(item)          # uses __str__
        print(repr(item))    # uses __repr__

    print("\n=== Available items ===")
    for item in library.list_available():
        print(item)

    print("\n=== Checkout / return demo ===")
    library.checkout("Dune")
    print(library.find_by_title("Dune"))

    try:
        library.checkout("Dune")  # should fail — already checked out
    except ValueError as e:
        print(f"Expected error: {e}")

    library.return_item("Dune")
    print(library.find_by_title("Dune"))

    print("\n=== Encapsulation check ===")
    dune = library.find_by_title("Dune")
    try:
        dune.status = "LOST"  # should fail — no public setter
    except AttributeError as e:
        print(f"Expected error: {e}")

    print("\n=== ISBN validation ===")
    print("0441013597 valid?", LibraryItem.is_valid_isbn10("0441013597"))
    print("1234567890 valid?", LibraryItem.is_valid_isbn10("1234567890"))

    print("\n=== Adding a new item + persisting ===")
    library.add_item(Book("Foundation", "Isaac Asimov", "0553293354"))
    library.save_to_database()
    print("Saved. Check database.txt.")


if __name__ == "__main__":
    main()