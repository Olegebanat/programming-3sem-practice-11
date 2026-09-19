import numpy as np

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-42"
N = 20

print(f"{STUDENT_NAME}, {STUDENT_GROUP}, N = {N}")


# Task 1
print("\n--- Task 1 ---")

data = np.arange(10, 10 + N)

print(data)
print(data[0], data[-1], data[-3], data[N // 2])

data[0] = 0
print(data)


# Task 2
print("\n--- Task 2 ---")

print(data[:3])
print(data[-3:])
print(data[::2])
print(data[::-1])
print(data[1:-1])


# Task 3
print("\n--- Task 3 ---")

view = data[:3]
copy = data[:3].copy()

view[0] = -100

print("data:", data)
print("view:", view)
print("copy:", copy)

print(view.base is data, copy.base is None)

# The view shares data with the original array,
# while the copy has its own independent data.


# Task 4
print("\n--- Task 4 ---")

table = np.arange(1, 21).reshape(4, 5)

print(table)

print(table[2, 3])
print(table[1])
print(table[:, 2])
print(table[1:3, 2:5])
print(table[-1, ::-1])


# Task 5
print("\n--- Task 5 ---")

frame = np.zeros((5, 5), dtype=int)

frame[0, :] = 1
frame[-1, :] = 1
frame[:, 0] = 1
frame[:, -1] = 1

frame[2, 2] = N

print(frame)


# Task 6
print("\n--- Task 6 ---")

temps = np.array([
    -3.5, -1.0, 4.5, 11.0,
    17.5, 22.0, 24.5, 23.0,
    18.0, 11.5, 5.0, -0.5
])

warm_mask = temps > N

print(warm_mask)
print(temps[warm_mask])
print(warm_mask.sum())
print(temps[warm_mask].mean())
print(np.where(warm_mask)[0])


# Task 7
print("\n--- Task 7 ---")

range_mask = (temps >= N) & (temps <= 2 * N)

print(temps[range_mask])
print(temps[~range_mask])

labels = np.where(
    temps > N,
    "warm",
    "cold"
)

print(labels)

no_negative = np.where(
    temps < 0,
    0.0,
    temps
)

print(no_negative)