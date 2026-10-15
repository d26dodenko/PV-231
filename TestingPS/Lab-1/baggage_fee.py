def calculate_baggage_fee(
    weight_kg: float,
    flight_type: str,
    is_premium: bool = False
) -> float:
    if weight_kg < 0:
        raise ValueError("weight_kg must be >= 0")

    if weight_kg > 50:
        raise ValueError("weight_kg must be <= 50")

    if flight_type not in ("domestic", "international"):
        raise ValueError("invalid flight_type")

    if weight_kg <= 10:
        cost = 0.0
    elif flight_type == "domestic":
        cost = (weight_kg - 10) * 150
    else:
        cost = (weight_kg - 10) * 250

    if weight_kg > 30:
        cost += 1000

    if is_premium:
        cost *= 0.7

    return round(cost, 2)
