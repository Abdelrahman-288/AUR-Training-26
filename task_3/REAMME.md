# Task 3 — Library Management System

## ISBN Validation
This project validates **ISBN-10** checksums (see `LibraryItem.is_valid_isbn10`).
Each digit (positions 0–9) is multiplied by (10 - position); the total must be
divisible by 11. The final character may be 'X' representing the value 10.

## SOLID Principles
- **SRP**: `Library` only manages the in-memory collection and checkout logic.
  `Database` only reads/writes `database.txt`. Neither does the other's job.
- **OCP**: Adding a new item type (e.g. `AudioBook`) only requires a new subclass
  decorated with `@LibraryItem.register("AudioBook")` and a `_build` classmethod.
  No changes are needed in `Library` or the dispatch logic in `from_dict`.
- **Encapsulation**: `_status` is a private attribute exposed only via a read-only
  `status` property. It can only change through `checkout()`, `return_item()`,
  and `mark_lost()`, each of which validates the transition.

## Running
```bash
python main.py
```# Task 3 — Library Management System

## ISBN Validation
This project validates **ISBN-10** checksums (see `LibraryItem.is_valid_isbn10`).
Each digit (positions 0–9) is multiplied by (10 - position); the total must be
divisible by 11. The final character may be 'X' representing the value 10.

## SOLID Principles
- **SRP**: `Library` only manages the in-memory collection and checkout logic.
  `Database` only reads/writes `database.txt`. Neither does the other's job.
- **OCP**: Adding a new item type (e.g. `AudioBook`) only requires a new subclass
  decorated with `@LibraryItem.register("AudioBook")` and a `_build` classmethod.
  No changes are needed in `Library` or the dispatch logic in `from_dict`.
- **Encapsulation**: `_status` is a private attribute exposed only via a read-only
  `status` property. It can only change through `checkout()`, `return_item()`,
  and `mark_lost()`, each of which validates the transition.

## Running
```bash
python main.py
```