stock_inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity or type quit: ")

    if user_input.lower() == "quit":
        print("Total units processed:", stock_inventory)
        print("Total number of failed entries:", failed_entries)
        break

    elif user_input.isdigit():
        stock_quantity = int(user_input)

        if stock_inventory + stock_quantity > 500:
            print("Alert: The total inventory exceeds 500 units.")
            print("Inventory before the rejected entry:", stock_inventory)
            print("Total number of failed entries:", failed_entries)
            break
        else:
            stock_inventory = stock_inventory + stock_quantity
            print("The total units processed is", stock_inventory)

    else:
        print("Entry rejected. Please enter a positive integer.")
        failed_entries = failed_entries + 1