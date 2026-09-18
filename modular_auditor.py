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