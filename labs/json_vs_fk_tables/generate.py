import random

with open('hashtags_insert.sql', 'w') as file:
    file.write('INSERT INTO tests.hashtags (datalist) values\n')

    for n in range(1024):
        numbers = [random.randint(-50, +50) for _ in range(random.randint(2, 10))]
        file.write(f"('{str(numbers)}')")
        file.write(',\n' if n < 1023 else ';')
