import random

def generate_random_array(length):
    random_array = []
    for _ in range(length):
        random_number = random.randint(10, 150)
        random_array.append(random_number)
    return random_array
# Ejemplo de uso
# length = 5
# result = generate_random_array(length)