stock_inventory = 0
failed_entries = 0
deliveries_processed = 0


def get_valid_input():
    user_input = input("Enter stock quantity or type quit: ")

    if user_input.lower() == "quit":
        return "quit"

    elif user_input.isdigit():
        return int(user_input)

    else:
        print("Entry rejected. Please enter a positive integer.")
        return "invalid"


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total units processed:", total_units)
    print("Total number of failed entries:", failed_attempts)


while True:
    stock_quantity = get_valid_input()

    if stock_quantity == "quit":
        break

    elif stock_quantity == "invalid":
        failed_entries = failed_entries + 1

    elif stock_inventory + stock_quantity > 500:
        print("Alert: The total inventory exceeds 500 units.")
        print("Inventory before the rejected entry:", stock_inventory)

        failed_entries = failed_entries + 1
        break

    else:
        stock_inventory = process_delivery(stock_inventory,stock_quantity)

        tax = calculate_tax(stock_quantity)
        deliveries_processed = deliveries_processed + 1

        print("The total units processed is", stock_inventory)
        print("Tax for this delivery is", tax)


print("\nTotal deliveries processed:", deliveries_processed)
generate_report(stock_inventory, failed_entries)