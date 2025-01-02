from functools import cache

TEST_INPUT = """125 17"""


@cache
def count_stones(stone_value, iteration=0):
	# Set max_iter to 25 for part A, and to 75 for part B
	max_iter = 75

	if iteration == max_iter:
		return 1

	if stone_value == 0:
		return count_stones(1, iteration + 1)

	elif len(str(stone_value)) % 2 == 0:
		midpoint = int(len(str(stone_value)) / 2)
		left_half = int(str(stone_value)[:midpoint])
		right_half = int(str(stone_value)[midpoint:])
		return count_stones(left_half, iteration + 1) + count_stones(right_half, iteration + 1)

	else:
		return count_stones(stone_value * 2024, iteration + 1)


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

# Part A and B
total_stones = 0
for stone in REAL_INPUT.split():
	total_stones += count_stones(int(stone))
print(total_stones)
