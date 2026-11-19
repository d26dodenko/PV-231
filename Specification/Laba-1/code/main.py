from salary import calculate_salary


if __name__ == "__main__":
    result = calculate_salary(160000, 170, 1.5, True)
    print(f"Итоговая зарплата: {result:.2f}")
