def load_inventory():
    inventory_file = open("inventory.txt", "a")
    inventory_file.close()

    inventory_file = open("inventory.txt", "r")

    saved_total = 0
    order_history = []

    for line in inventory_file:
        line = line.strip()

        if line != "":
            order_details = line.split(",")

            if (
                len(order_details) == 2
                and order_details[0] == "TOTAL"
                and order_details[1].isdigit()
            ):
                saved_total = int(order_details[1])

            elif (
                len(order_details) == 3
                and order_details[0].strip().isdigit()
                and order_details[2].strip().isdigit()
                and int(order_details[0].strip()) >= 1001
            ):
                product_number = int(
                    order_details[0].strip()
                )
                product_name = order_details[1].strip()
                product_quantity = int(
                    order_details[2].strip()
                )

                order_history.append(
                    [
                        product_number,
                        product_name,
                        product_quantity
                    ]
                )

    inventory_file.close()

    if len(order_history) == 0:
        print("No saved inventory found.")
        print("Starting with an empty inventory.")

    else:
        print("Current Orders:\n")

        for order in order_history:
            print(
                str(order[0])
                + ", "
                + order[1]
                + ", "
                + str(order[2])
            )

    return saved_total, order_history


def save_inventory(total_quantity, order_history):
    inventory_file = open("inventory.txt", "w")

    inventory_file.write(
        "TOTAL," + str(total_quantity) + "\n"
    )

    for order in order_history:
        inventory_file.write(
            str(order[0])
            + ","
            + order[1]
            + ","
            + str(order[2])
            + "\n"
        )

    inventory_file.close()

    print(
        "\nOrder successfully saved to inventory.txt"
    )


def get_product_name():
    product_name = input(
        "\nEnter Product Name or type quit: "
    ).strip()

    if product_name.lower() == "quit":
        return "quit"

    elif product_name == "":
        print("Product name cannot be empty.")

        return "invalid"

    elif "," in product_name:
        print("Product name cannot contain a comma.")

        return "invalid"

    else:
        return product_name


def get_valid_quantity():
    quantity_input = input(
        "Enter Quantity: "
    ).strip()

    if (
        quantity_input.isdigit()
        and int(quantity_input) > 0
    ):
        return int(quantity_input)

    else:
        print(
            "Entry rejected. Please enter a positive integer."
        )

        return "invalid"


def generate_product_number(order_history):
    if len(order_history) == 0:
        return 1001

    highest_product_number = order_history[0][0]

    for order in order_history:
        if order[0] > highest_product_number:
            highest_product_number = order[0]

    return highest_product_number + 1


def process_order(
    order_history,
    product_number,
    product_name,
    product_quantity
):
    new_order = [
        product_number,
        product_name,
        product_quantity
    ]

    order_history.append(new_order)

    return new_order


def display_new_order(new_order):
    print("\nNew Order Added:")

    print(
        str(new_order[0])
        + ","
        + new_order[1]
        + ","
        + str(new_order[2])
    )


total_quantity, order_history = load_inventory()

while True:
    product_name = get_product_name()

    if product_name == "quit":
        save_inventory(
            total_quantity,
            order_history
        )

        break

    elif product_name == "invalid":
        continue

    product_quantity = get_valid_quantity()

    if product_quantity == "invalid":
        continue

    product_number = generate_product_number(
        order_history
    )

    new_order = process_order(
        order_history,
        product_number,
        product_name,
        product_quantity
    )

    total_quantity = (
        total_quantity + product_quantity
    )

    display_new_order(new_order)