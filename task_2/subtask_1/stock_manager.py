def load_stock(filename):
    stock = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 2:
                    raise ValueError

                name = parts[0].strip().lower()
                quantity = int(parts[1].strip())

                if not name or quantity < 0:
                    raise ValueError

                stock[name] = quantity

    except FileNotFoundError:
        print("Error: stock.txt was not found.")
        return None

    except (ValueError, OSError):
        print("Error: stock.txt has a corrupted format.")
        return None

    return stock


def save_stock(filename, stock):
    with open(filename, "w") as file:
        for name, quantity in stock.items():
            file.write(f"{name},{quantity}\n")


def show_stock(stock):
    if not stock:
        print("Stock is empty.")
        return

    for index, (name, quantity) in enumerate(stock.items(), start=1):
        print(f"{index}. {name}: {quantity}")


def get_stock_item(stock):
    while True:
        choice = input("Enter the stock name or ID: ").strip()

        if choice.isdigit():
            item_id = int(choice)

            if 1 <= item_id <= len(stock):
                return list(stock.keys())[item_id - 1]

            print("Invalid ID. Please try again.")

        else:
            name = choice.lower()

            if name in stock:
                return name

            print("Stock item not found. Please try again.")


def get_quantity():
    while True:
        value = input("Enter the quantity: ").strip()

        try:
            quantity = int(value)

            if quantity < 0:
                print("Quantity cannot be negative.")
            else:
                return quantity

        except ValueError:
            print("Please enter a valid number.")


def add_stock(stock):
    show_stock(stock)

    choice = input(
        "Enter the stock name or ID, or enter a new stock name: "
    ).strip()

    if choice.isdigit():
        item_id = int(choice)

        if 1 <= item_id <= len(stock):
            name = list(stock.keys())[item_id - 1]
        else:
            print("Invalid ID.")
            return
    else:
        name = choice.lower()

    if not name:
        print("Stock name cannot be empty.")
        return

    quantity = get_quantity()

    if name in stock:
        stock[name] += quantity
    else:
        stock[name] = quantity

    print(f"{quantity} added to {name}.")


def remove_stock(stock):
    show_stock(stock)

    name = get_stock_item(stock)
    quantity = get_quantity()

    if quantity > stock[name]:
        print("Cannot remove more stock than available.")
        return

    stock[name] -= quantity

    print(f"{quantity} removed from {name}.")


def print_menu():
    print("\n1. Add stock")
    print("2. Remove stock")
    print("3. Show stock")
    print("4. Exit")


def main():
    filename = "stock.txt"
    stock = load_stock(filename)

    if stock is None:
        return

    while True:
        print_menu()

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            add_stock(stock)

        elif choice == "2":
            remove_stock(stock)

        elif choice == "3":
            show_stock(stock)

        elif choice == "4":
            save_stock(filename, stock)
            print("Stock saved. Exiting program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()