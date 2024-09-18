import time


def fibonacci(number: int) -> int:
    """Рекурсивная функция вычисляющая n-й элемент ряда Фибоначчи
    """
    if number < 2:
        return number
    return fibonacci(number - 1) + fibonacci(number - 2)


if __name__ == '__main__':
    s = time.time()
    fibonacci(38)
    print(time.time() - s)
