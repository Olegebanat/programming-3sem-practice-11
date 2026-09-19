import numpy as np

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-42"
N = 20

print(f"{STUDENT_NAME}, {STUDENT_GROUP}, N = {N}")


# Task 1
print("\n--- Task 1 ---")

a = np.arange(1, N + 1)

print(a)
print("Shape:", a.shape)
print("Size:", a.size)
print("Dtype:", a.dtype)


# Task 2
print("\n--- Task 2 ---")

zeros_array = np.zeros((3, 4))
ones_array = np.ones((2, N), dtype=int)
full_array = np.full((2, 2), N)
identity_matrix = np.eye(N)

print("Zeros:")
print(zeros_array)

print("Ones:")
print(ones_array)

print("Filled with N:")
print(full_array)

print("Identity matrix:")
print(identity_matrix)


# Task 3
print("\n--- Task 3 ---")

points = np.linspace(0, 1, N)
even_numbers = np.arange(0, 21, 2)

print("Linspace:")
print(points)

print("Even numbers:")
print(even_numbers)


# Task 4
print("\n--- Task 4 ---")

numbers = np.arange(1, 13)
print("Original:")
print(numbers)

matrix_3x4 = numbers.reshape(3, 4)
print("3x4:")
print(matrix_3x4)
print("Shape:", matrix_3x4.shape)

matrix_4x3 = numbers.reshape(4, 3)
print("4x3:")
print(matrix_4x3)
print("Shape:", matrix_4x3.shape)

matrix_2x_auto = numbers.reshape(2, -1)
print("2x-auto:")
print(matrix_2x_auto)
print("Shape:", matrix_2x_auto.shape)


# Task 5
print("\n--- Task 5 ---")

print("a * 2:")
print(a * 2)

print("a + 10:")
print(a + 10)

print("a ** 2:")
print(a ** 2)

print("a / N:")
print(a / N)

sum_of_squares = (a ** 2).sum()

print("Sum of squares:")
print(sum_of_squares)


# Task 6
print("\n--- Task 6 ---")

temps = np.array([
    16.5, 18.0, 21.5, 23.0, 19.5, 24.5, 22.0
])

print("Temperatures:")
print(temps)

print("Minimum:")
print(temps.min())

print("Maximum:")
print(temps.max())

print("Average:")
print(temps.mean())

print("Warmest day index:")
print(temps.argmax())

warm_days = temps > N

print("Warm days:")
print(warm_days)

print("Number of warm days:")
print(warm_days.sum())

fahrenheit = temps * 9 / 5 + 32

print("Fahrenheit:")
print(fahrenheit)


# Task 7
print("\n--- Task 7 ---")

print("Matrix:")
print(matrix_3x4)

print("Sum of all elements:")
print(matrix_3x4.sum())

print("Sum by columns:")
print(matrix_3x4.sum(axis=0))

print("Sum by rows:")
print(matrix_3x4.sum(axis=1))