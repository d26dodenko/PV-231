def calculate_book_delivery(order_amount: float, weight_kg: float, is_premium: bool) -> float:
    if type(order_amount) not in (int, float):
        raise TypeError("order_amount must be a number")
    if type(weight_kg) not in (int, float):
        raise TypeError("weight_kg must be a number")
    if type(is_premium) is not bool:
        raise TypeError("is_premium must be a boolean")

    if order_amount < 0:
        raise ValueError("order_amount must be non-negative")
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")

    if order_amount >= 3500:
        return 0.0

    if weight_kg <= 2:
        cost = 180.0
    elif weight_kg <= 5:
        cost = 280.0
    else:
        cost = 280.0 + (weight_kg - 5) * 50.0

    if is_premium:
        cost *= 0.75

    return round(cost, 2)
