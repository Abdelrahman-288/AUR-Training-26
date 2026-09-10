from abc import ABC, abstractmethod
from enums import ItemStatus


class LibraryItem(ABC):
    """Abstract base class for all library items."""

    _registry = {}  # type_name (str) -> concrete class

    def __init__(self, title):
        self.title = title
        self._status = ItemStatus.AVAILABLE

    # ---------- registry / OCP machinery ----------
    @classmethod
    def register(cls, type_name):
        def decorator(subclass):
            cls._registry[type_name] = subclass
            return subclass
        return decorator

    @classmethod
    def from_dict(cls, data):
        item_type = data.get("type")
        target_cls = cls._registry.get(item_type)
        if target_cls is None:
            raise ValueError(f"Unknown item type: {item_type}")
        return target_cls._build(data)

    @classmethod
    def _build(cls, data):
        """Each subclass must implement this to parse its own fields."""
        raise NotImplementedError

    # ---------- encapsulated status ----------
    @property
    def status(self):
        return self._status

    def checkout(self):
        if self._status != ItemStatus.AVAILABLE:
            raise ValueError(f"Cannot check out '{self.title}': currently {self._status.value}.")
        self._status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self._status != ItemStatus.CHECKED_OUT:
            raise ValueError(f"Cannot return '{self.title}': it is not checked out.")
        self._status = ItemStatus.AVAILABLE

    def mark_lost(self):
        self._status = ItemStatus.LOST

    # ---------- abstract polymorphic behaviour ----------
    @property
    @abstractmethod
    def loan_period_days(self):
        ...

    def to_dict(self):
        """Base fields common to every item; subclasses extend this."""
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "status": self._status.value,
        }

    # ---------- comparison / printing ----------
    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r}, status={self._status.name})"

    def __str__(self):
        return f"{self.title} ({self.__class__.__name__}) — {self._status.value.title()}"

    # ---------- static ISBN validator ----------
    @staticmethod
    def is_valid_isbn10(isbn: str) -> bool:
        """
        Validates an ISBN-10 checksum.
        Rule: sum(digit_i * (10 - i)) for i in 0..9 must be divisible by 11.
        The last character may be 'X' representing the value 10.
        """
        isbn = isbn.replace("-", "").strip()
        if len(isbn) != 10:
            return False

        total = 0
        for i, ch in enumerate(isbn):
            if ch.upper() == "X" and i == 9:
                value = 10
            elif ch.isdigit():
                value = int(ch)
            else:
                return False
            total += value * (10 - i)

        return total % 11 == 0


@LibraryItem.register("Book")
class Book(LibraryItem):
    def __init__(self, title, author, isbn):
        super().__init__(title)
        self.author = author
        self.isbn = isbn

    @property
    def loan_period_days(self):
        return 21

    @classmethod
    def _build(cls, data):
        item = cls(data["title"], data["author"], data["isbn"])
        item._status = ItemStatus[data["status"]]
        return item

    def to_dict(self):
        base = super().to_dict()
        base.update({"author": self.author, "isbn": self.isbn})
        return base


@LibraryItem.register("DVD")
class DVD(LibraryItem):
    def __init__(self, title, director):
        super().__init__(title)
        self.director = director

    @property
    def loan_period_days(self):
        return 5

    @classmethod
    def _build(cls, data):
        item = cls(data["title"], data["director"])
        item._status = ItemStatus[data["status"]]
        return item

    def to_dict(self):
        base = super().to_dict()
        base.update({"director": self.director})
        return base


@LibraryItem.register("Magazine")
class Magazine(LibraryItem):
    def __init__(self, title, issue):
        super().__init__(title)
        self.issue = issue

    @property
    def loan_period_days(self):
        return 14

    @classmethod
    def _build(cls, data):
        item = cls(data["title"], data["issue"])
        item._status = ItemStatus[data["status"]]
        return item

    def to_dict(self):
        base = super().to_dict()
        base.update({"issue": self.issue})
        return base