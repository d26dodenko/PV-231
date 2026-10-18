def calculate_salary(
    base_salary: float,
    worked_hours: int,
    overtime_rate: float,
    has_bonus: bool
) -> float:
    if base_salary < 0:
        raise ValueError("base_salary must be >= 0")
    if worked_hours < 0:
        raise ValueError("worked_hours must be >= 0")
    if overtime_rate < 0:
        raise ValueError("overtime_rate must be >= 0")

    salary = float(base_salary)

    if worked_hours < 80:
        salary *= 0.8

    if worked_hours > 160:
        hourly_rate = base_salary / 160
        overtime_hours = worked_hours - 160
        salary += overtime_hours * hourly_rate * overtime_rate

    if has_bonus and worked_hours >= 160:
        salary *= 1.2

    return max(0.0, salary)


if __name__ == "__main__":
    result = calculate_salary(160000, 170, 1.5, True)
    print(f"Итоговая зарплата: {result:.2f}")