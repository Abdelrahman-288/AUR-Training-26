class Database:
    """
    Responsible ONLY for reading/writing the collection to database.txt.
    Implemented as a singleton so every part of the program shares one instance.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filepath="database.txt"):
        if not hasattr(self, "_initialized"):
            self.filepath = filepath
            self._initialized = True

    def load(self):
        """Reads database.txt and returns a list of dicts (one per line)."""
        records = []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    fields = dict(pair.split("=", 1) for pair in line.split("|"))
                    records.append(fields)
        except FileNotFoundError:
            pass
        return records

    def save(self, items):
        """Writes a list of LibraryItem objects back to database.txt."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            for item in items:
                data = item.to_dict()
                line = "|".join(f"{key}={value}" for key, value in data.items())
                f.write(line + "\n")