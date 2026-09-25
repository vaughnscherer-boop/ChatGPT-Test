"""Simple cash register. Run with: python3 cash_register.py"""

import re

MENU = {"1": ("Hot Dog", 500), "2": ("Hamburger", 600), "3": ("Shake", 1000)}


def money(cents):
    return f"${cents // 100}.{cents % 100:02d}"


def parse_cash(value):
    """Convert dollars to integer cents without floating-point rounding."""
    value = value.strip().removeprefix("$")
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", value):
        raise ValueError("Enter a positive dollar amount, such as 20 or 20.50.")
    dollars, _, cents = value.partition(".")
    amount = int(dollars) * 100 + int(cents.ljust(2, "0"))
    if amount <= 0:
        raise ValueError("The payment must be greater than zero.")
    return amount


def checkout(cart):
    total = sum(MENU[key][1] * quantity for key, quantity in cart.items())
    print("\n--- Receipt ---")
    for key, quantity in cart.items():
        name, price = MENU[key]
        print(f"{quantity} x {name} @ {money(price)} = {money(price * quantity)}")
    print(f"Total: {money(total)} (no tax added)")
    paid = 0
    while paid < total:
        print(f"Amount due: {money(total - paid)}")
        value = input("Cash received (or C to cancel): ").strip()
        if value.lower() == "c":
            print(f"Sale canceled. Return {money(paid)} to the customer.")
            return
        try:
            paid += parse_cash(value)
        except ValueError as error:
            print(error)
            continue
        if paid < total:
            print(f"Payment received: {money(paid)}. Please add more cash.")
    print(f"Cash received: {money(paid)}")
    print(f"Change to return: {money(paid - total)}")
    print("Thank you! Sale complete.")


def main():
    print("Welcome to the Store Cash Register!")
    cart = {}
    while True:
        print("\n--- Menu ---")
        for key, (name, price) in MENU.items():
            print(f"{key}. {name}: {money(price)}")
        print("4. Checkout\n5. Clear order\n6. Exit")
        total = sum(MENU[key][1] * quantity for key, quantity in cart.items())
        print(f"Current total: {money(total)}")
        choice = input("Choose an option: ").strip()
        if choice in MENU:
            try:
                quantity = int(input("Quantity: "))
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                print("Please enter a positive whole-number quantity.")
                continue
            cart[choice] = cart.get(choice, 0) + quantity
            print(f"Added {quantity} x {MENU[choice][0]}.")
        elif choice == "4":
            if not cart:
                print("Add an item before checking out.")
                continue
            checkout(cart)
            cart = {}
        elif choice == "5":
            cart = {}
            print("Order cleared.")
        elif choice == "6":
            print("Register closed.")
            return
        else:
            print("Please choose an option from 1 to 6.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nRegister interrupted. If cash was collected for an unfinished sale, return it.")
