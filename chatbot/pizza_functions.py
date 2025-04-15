class PizzaFunctions:
    _current_orders = []
    _menu = {
        "pizzas": [
            {"name": "Margherita", "sizes": {"small": 10.99, "medium": 12.99, "large": 14.99}},
            {"name": "Pepperoni", "sizes": {"small": 11.99, "medium": 13.99, "large": 15.99}},
            {"name": "Vegetarian", "sizes": {"small": 11.99, "medium": 13.99, "large": 15.99}},
            {"name": "Hawaiian", "sizes": {"small": 12.99, "medium": 14.99, "large": 16.99}},
            {"name": "Supreme", "sizes": {"small": 13.99, "medium": 15.99, "large": 17.99}}
        ],
        "drinks": [
            {"name": "Cola", "sizes": {"small": 1.99, "medium": 2.49, "large": 2.99}},
            {"name": "Lemonade", "sizes": {"small": 1.99, "medium": 2.49, "large": 2.99}},
            {"name": "Iced Tea", "sizes": {"small": 1.99, "medium": 2.49, "large": 2.99}},
            {"name": "Water", "sizes": {"small": 0.99, "medium": 1.49, "large": 1.99}}
        ]
    }

    @classmethod
    def get_menu(cls) -> str:
        menu_str = "Pizza Menu:\n"
        for pizza in cls._menu["pizzas"]:
            menu_str += f"{pizza['name']}:\n"
            for size, price in pizza['sizes'].items():
                menu_str += f"  {size.capitalize()}: ${price:.2f}\n"
            menu_str += "\n"

        menu_str += "Drinks Menu:\n"
        for drink in cls._menu["drinks"]:
            menu_str += f"{drink['name']}:\n"
            for size, price in drink['sizes'].items():
                menu_str += f"  {size.capitalize()}: ${price:.2f}\n"
            menu_str += "\n"
        return menu_str

    @classmethod
    def insert_order(cls, name: str, size: str, quantity: int) -> str:
        price = None
        for category in ["pizzas", "drinks"]:
            for item in cls._menu[category]:
                if item["name"].lower() == name.lower():
                    price = item["sizes"].get(size.lower())
                    break
            if price is not None:
                break

        if price is None:
            return f"Item '{name}' with size '{size}' not found in the menu."

        new_order = {
            "name": name,
            "size": size.lower(),
            "quantity": quantity,
            "price": price
        }
        cls._current_orders.append(new_order)
        return f"Added {quantity} {size} {name}(s) to order."

    @classmethod
    def get_orders(cls):
        if not cls._current_orders:
            return "No current orders yet."
        order_list = "Current Orders:\n"
        for item in cls._current_orders:
            order_list += f"{item['quantity']}x {item['size'].capitalize()} {item['name']} - ${item['price']:.2f} each\n"
        return order_list

    @classmethod
    def finalize_orders(cls) -> str:
        if not cls._current_orders:
            return "Order is empty. Please add some items before finalizing."

        order_summary = "Order summary:\n"
        total = 0
        for item in cls._current_orders:
            item_total = item["quantity"] * item["price"]
            total += item_total
            order_summary += f"{item['quantity']}x {item['size'].capitalize()} {item['name']}: ${item_total:.2f}\n"

        order_summary += f"\nTotal: ${total:.2f}"
        cls._current_orders = []
        return order_summary

    @classmethod
    def clear_orders(cls):
        cls._current_orders = []
