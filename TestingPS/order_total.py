def calculate_order_total(item_price, quantity, user_type, delivery_cost):
    if not isinstance(item_price, (int, float)) or isinstance(item_price, bool):
        raise ValueError("item_price must be a number")
    if item_price <= 0:
        raise ValueError("item_price must be > 0")

    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError("quantity must be an integer")
    if quantity < 1 or quantity > 100:
        raise ValueError("quantity must be between 1 and 100")

    if user_type not in ("regular", "premium"):
        raise ValueError("user_type must be 'regular' or 'premium'")

    if not isinstance(delivery_cost, (int, float)) or isinstance(delivery_cost, bool):
        raise ValueError("delivery_cost must be a number")
    if delivery_cost < 0:
        raise ValueError("delivery_cost must be >= 0")

    subtotal = item_price * quantity
    discount = subtotal * 0.10 if user_type == "premium" else 0.0
    total_after_discount = subtotal - discount
    delivery = 0.0 if subtotal >= 2000 else delivery_cost

    return round(total_after_discount + delivery, 2)
