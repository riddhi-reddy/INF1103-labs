def load_inventory():
    inventory_file = open("inventory.txt", "a")
    inventory_file.close()

    inventory_file = open("inventory.txt", "r")
    saved_total = inventory_file.readline().strip()
    history_line = inventory_file.readline().strip()
    inventory_file.close()

    if saved_total == "":
        print("No saved inventory found.")
        print("Starting with an empty inventory.")

        return 0, []

    saved_total = int(saved_total)

    if history_line == "":
        saved_history = []
    else:
        saved_history = history_line.split(",")

        for index in range(len(saved_history)):
            saved_history[index] = int(saved_history[index])

    print("Previous inventory loaded successfully.")
    print("Current inventory:", saved_total)
    print("Transaction history:", saved_history)

    return saved_total, saved_history
    
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
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * 0.10
    return tax

def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total units processed:", total_units)
    print("Total number of failed entries:", failed_attempts)


stock_inventory, transaction_history = load_inventory()
failed_entries = 0
deliveries_processed = 0

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

        transaction_history.append(stock_quantity)

        tax = calculate_tax(stock_quantity)
        deliveries_processed = deliveries_processed + 1

        print("The total units processed is", stock_inventory)
        print("Tax for this delivery is", tax)
        print("Transaction history:", transaction_history)


print("Total deliveries processed:", deliveries_processed)
generate_report(stock_inventory, failed_entries)