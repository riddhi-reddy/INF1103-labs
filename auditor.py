inventory = 0
failed_entries = 0 

while True: 
    stock_quantity = input("Enter Stock Quantity (Type 'quit' to quit): ")
    if stock_quantity.lower() == "quit": 
        print("Total Units Processed:", inventory)
        break

    if not stock_quantity.isdigit():
        print("The number is rejected.")
        failed_entries += 1
        continue
    
    actual = int(stock_quantity)
    inventory += actual

    if actual < 0:
        print("Rejects negative numbers")
        failed_entries += 1
        continue

    elif inventory > 500:
        print("Alert, overloaded")
        inventory -= actual
        break
print("Total Units Processed: ", inventory)
print("Number of Failed/Refected Entries: ", failed_entries)