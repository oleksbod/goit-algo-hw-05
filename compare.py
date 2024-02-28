import timeit
import os

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

# Knuth-Morris-Pratt algorithm
def knuth_morris_pratt(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Boyer-Moore algorithm
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

# Rabin-Karp algorithm
def rabin_karp(text, pattern):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(pattern)
    main_string_length = len(text)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i+substring_length] == pattern:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# функція для заміру часу
def measure_time(algorithm, text, pattern):
    start_time = timeit.default_timer()
    algorithm(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time


# Article 1
print("\nArticle 1\n")
script_directory = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(script_directory, "article1.txt")
text_data = open(text_file_path, 'r').read()

# Generate a valid substring that exists in the text
existing_substring = "кількість"

# Generate a random substring that doesn't exist in the text
random_substring = "sdfkoxsqajiwefb"

# Measure time for each algorithm with the existing substring
time_boyer_moore_existing = measure_time(boyer_moore, text_data, existing_substring)
time_knuth_morris_pratt_existing = measure_time(knuth_morris_pratt, text_data, existing_substring)
time_rabin_karp_existing = measure_time(rabin_karp, text_data, existing_substring)

# Measure time for each algorithm with the random substring
time_boyer_moore_random = measure_time(boyer_moore, text_data, random_substring)
time_knuth_morris_pratt_random = measure_time(knuth_morris_pratt, text_data, random_substring)
time_rabin_karp_random = measure_time(rabin_karp, text_data, random_substring)

# Print the results
print("Existing Substring:")
print(f"Boyer-Moore: {time_boyer_moore_existing:.6f} seconds")
print(f"Knuth-Morris-Pratt: {time_knuth_morris_pratt_existing:.6f} seconds")
print(f"Rabin-Karp: {time_rabin_karp_existing:.6f} seconds")

print("\nRandom Substring:")
print(f"Boyer-Moore: {time_boyer_moore_random:.6f} seconds")
print(f"Knuth-Morris-Pratt: {time_knuth_morris_pratt_random:.6f} seconds")
print(f"Rabin-Karp: {time_rabin_karp_random:.6f} seconds")


# Article 2
print("\nArticle 2\n")
script_directory = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(script_directory, "article2.txt")
text_data = open(text_file_path, 'r').read()

# Generate a valid substring that exists in the text
existing_substring = "кількість"

# Generate a random substring that doesn't exist in the text
random_substring = "sdfkoxsqajiwefb"

# Measure time for each algorithm with the existing substring
time_boyer_moore_existing = measure_time(boyer_moore, text_data, existing_substring)
time_knuth_morris_pratt_existing = measure_time(knuth_morris_pratt, text_data, existing_substring)
time_rabin_karp_existing = measure_time(rabin_karp, text_data, existing_substring)

# Measure time for each algorithm with the random substring
time_boyer_moore_random = measure_time(boyer_moore, text_data, random_substring)
time_knuth_morris_pratt_random = measure_time(knuth_morris_pratt, text_data, random_substring)
time_rabin_karp_random = measure_time(rabin_karp, text_data, random_substring)

# Print the results
print("Existing Substring:")
print(f"Boyer-Moore: {time_boyer_moore_existing:.6f} seconds")
print(f"Knuth-Morris-Pratt: {time_knuth_morris_pratt_existing:.6f} seconds")
print(f"Rabin-Karp: {time_rabin_karp_existing:.6f} seconds")

print("\nRandom Substring:")
print(f"Boyer-Moore: {time_boyer_moore_random:.6f} seconds")
print(f"Knuth-Morris-Pratt: {time_knuth_morris_pratt_random:.6f} seconds")
print(f"Rabin-Karp: {time_rabin_karp_random:.6f} seconds")