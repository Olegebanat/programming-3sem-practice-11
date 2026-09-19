import numpy as np

STUDENT_NAME = "Yulian Mykhalchuk"
STUDENT_GROUP = "IT-42"
N = 20

rng = np.random.default_rng(N)

print(f"{STUDENT_NAME}, {STUDENT_GROUP}, N = {N}")


# Task 1
print("\n--- Task 1 ---")

A = np.array([
    [2, 1, -1],
    [1, 3, 2],
    [3, -1, 1]
], dtype=float)

b = np.array([N, 2 * N, 10], dtype=float)

x = np.linalg.solve(A, b)

print("Solution:")
print(x)

print("A @ x:")
print(A @ x)

print("Check:")
print(np.allclose(A @ x, b))


# Task 2
print("\n--- Task 2 ---")

M = np.array([
    [N, 2],
    [1, 3]
], dtype=float)

print("M:")
print(M)

print("M * M:")
print(M * M)

print("M @ M:")
print(M @ M)

# M * M performs element-wise multiplication,
# while M @ M performs matrix multiplication.

det_M = np.linalg.det(M)
print("Determinant:")
print(round(det_M, 2))

inv_M = np.linalg.inv(M)
print("Inverse matrix:")
print(inv_M)

print("Identity check:")
print(np.allclose(M @ inv_M, np.eye(2)))


# Task 3
print("\n--- Task 3 ---")

grades = np.array([
    95, 82, 57, 74, 91,
    48, 66, 88, 53, 100
])

print("Grades:")
print(grades)

print("Mean:")
print(round(grades.mean(), 2))

print("Median:")
print(round(np.median(grades), 2))

print("Standard deviation:")
print(round(grades.std(), 2))

print("Minimum:")
print(grades.min())

print("Maximum:")
print(grades.max())

print("Failed count:")
print((grades < 60).sum())

print("Grades >= 90:")
print(grades[grades >= 90])

print("Student number with highest grade:")
print(grades.argmax() + 1)


# Task 4
print("\n--- Task 4 ---")

rolls = rng.integers(1, 7, size=1000)

print("First 10 rolls:")
print(rolls[:10])

counts = np.bincount(rolls, minlength=7)[1:]

print("Face counts:")
print(counts)

print("Mean:")
print(round(rolls.mean(), 4))

print("Theoretical mean:")
print(3.5)

six_ratio = (rolls == 6).mean()

print("Six ratio:")
print(round(six_ratio, 4))

print("Theoretical six ratio:")
print(round(1 / 6, 4))


# Task 5
print("\n--- Task 5 ---")

two_dice = rng.integers(1, 7, size=(10_000, 2))
sums = two_dice.sum(axis=1)

sum_counts = np.bincount(sums, minlength=13)[2:13]

print("Counts for sums 2-12:")
print(sum_counts)

most_common_sum = np.argmax(sum_counts) + 2

print("Most common sum:")
print(most_common_sum)

probability_7 = (sums == 7).mean()

print("Probability of sum 7:")
print(round(probability_7, 4))

print("Theoretical probability of sum 7:")
print(round(6 / 36, 4))

probability_10_or_more = (sums >= 10).mean()

print("Probability of sum >= 10:")
print(round(probability_10_or_more, 4))


# Task 6
print("\n--- Task 6 ---")

group_grades = rng.normal(
    70,
    12,
    size=(N + 20, 3)
)

group_grades = np.rint(group_grades)
group_grades = np.clip(group_grades, 0, 100)
group_grades = group_grades.astype(int)

print("Shape:")
print(group_grades.shape)

print("First 3 students:")
print(group_grades[:3])

subject_means = group_grades.mean(axis=0)

print("Subject means:")
print(np.round(subject_means, 2))

student_means = group_grades.mean(axis=1)

best_student = student_means.argmax()

print("Best student number:")
print(best_student + 1)

print("Best student mean:")
print(round(student_means[best_student], 2))

failed_students = (student_means < 60).sum()

print("Students with mean < 60:")
print(failed_students)