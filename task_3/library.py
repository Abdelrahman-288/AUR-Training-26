from enums import ItemStatus
from library_item import LibraryItem


class Library:
    """
    Manages the in-memory collection and checkout/return logic.
    Contains NO file I/O — persistence is delegated to a Database instance.
    """

    def __init__(self, database):
        self._items = []
        self._database = database

    def add_item(self, item):
        self._items.append(item)

    def find_by_title(self, title):
        for item in self._items:
            if item.title == title:
                return item
        raise LookupError(f"No item titled '{title}' found.")

    def checkout(self, title):
        item = self.find_by_title(title)
        item.checkout()
        return item

    def return_item(self, title):
        item = self.find_by_title(title)
        item.return_item()
        return item

    def mark_lost(self, title):
        item = self.find_by_title(title)
        item.mark_lost()
        return item

    def list_available(self):
        return sorted(i for i in self._items if i.status == ItemStatus.AVAILABLE)

    def all_items(self):
        return sorted(self._items)

    def load_from_database(self):
        for record in self._database.load():
            self.add_item(LibraryItem.from_dict(record))

    def save_to_database(self):
        self._database.save(self._items)