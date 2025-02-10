import numpy as np
import re

TEST_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def parse_input(puzzle_input: str) -> np.array:
	puzzle_list = puzzle_input.split('\n')
	puzzle_array = [list(line) for line in puzzle_list]
	return np.array(puzzle_array)


def find_matches(line_to_search):
	# Returns number of overlapping and non-overlapping matches in a string with regex
	regex_str = r'(?=(XMAS))'
	return len(re.findall(regex_str, line_to_search))


def find_horizontal(array_):
	# Returns number of matches in horizontal (R to L; and L to R)
	count = 0
	for row in range(array_.shape[0]):
		result = str.join('', array_[row])
		result_reversed = result[::-1]
		count += find_matches(result)
		count += find_matches(result_reversed)
	return count


def find_vertical(array_):
	# Returns number of matches in vertical (U to D; D to U)
	count = 0
	for col in range(array_.shape[1]):
		result = str.join('', array_[:, col])
		result_reversed = result[::-1]
		count += find_matches(result)
		count += find_matches(result_reversed)
	return count


def find_diagonal(array_, anti_diagonal=False):
	# Returns number of matches in diagonal and diagonal backwards directions
	# If anti_diagonal is True; returns nuber of matches in anti-diag and anti-diag backwards directions

	if anti_diagonal:
		array_ = np.fliplr(array_)

	count = 0
	for i in range(0, array_.shape[1]):
		result = str.join('', array_.diagonal(i))
		result_reversed = result[::-1]
		count += find_matches(result)
		count += find_matches(result_reversed)

	for i in range(-1, -1 * array_.shape[0], -1):
		result = str.join('', array_.diagonal(i))
		result_reversed = result[::-1]
		count += find_matches(result)
		count += find_matches(result_reversed)

	return count


def is_x_mas(array_, i, j):
	"""
	Returns true if the "A" is in the middle of a valid X-MAS
	array[i_, j_] is the location of the "A" that is being tested

	There are four valid possibilities:

	-1,-1 = M and -1,1 = M and 1,-1 = S and 1, 1 = S (poss_1)
	M  M
	 A
	S  S

	-1,-1 = S and -1,1 = S and 1,-1 = M and 1, 1 = M (poss_2)
	S  S
	 A
	M  M

	-1,-1 = M and -1,1 = S and 1,-1 = M and 1, 1 = S (poss_3)
	M  S
	 A
	M  S

	-1,-1 = S and -1,1 = M and 1,-1 = S and 1, 1 = M (poss_4)
	S  M
	 A
	S  M
	"""

	poss_1 = (array_[i - 1, j - 1] == 'M' and array_[i - 1, j + 1] == 'M' and
			  array_[i + 1, j - 1] == 'S' and array_[i + 1, j + 1] == 'S')

	poss_2 = (array_[i - 1, j - 1] == 'S' and array_[i - 1, j + 1] == 'S' and
			  array_[i + 1, j - 1] == 'M' and array_[i + 1, j + 1] == 'M')

	poss_3 = (array_[i - 1, j - 1] == 'M' and array_[i - 1, j + 1] == 'S' and
			  array_[i + 1, j - 1] == 'M' and array_[i + 1, j + 1] == 'S')

	poss_4 = (array_[i - 1, j - 1] == 'S' and array_[i - 1, j + 1] == 'M' and
			  array_[i + 1, j - 1] == 'S' and array_[i + 1, j + 1] == 'M')

	if poss_1 or poss_2 or poss_3 or poss_4:
		return True
	else:
		return False


def count_x_mas(array_):
	# Returns count of valid X-mas's in the array
	count = 0
	for i in range(1, array_.shape[0] - 1):
		for j in range(1, array_.shape[1] - 1):
			if array_[i, j] == 'A' and is_x_mas(array_, i, j):
				count += 1
	return count


# Test input
# array = parse_input(TEST_INPUT)

# Real input
with open('input.txt', 'r') as f:
	INPUT = f.read()
array = parse_input(INPUT)

# PART A
horizontal = find_horizontal(array)
vertical = find_vertical(array)
diagonal = find_diagonal(array)
anti_diagonal = find_diagonal(array, anti_diagonal=True)
all_matches = horizontal + vertical + diagonal + anti_diagonal
print(f'{all_matches=}')

# PART B
all_x_mas = count_x_mas(array)
print(f'{all_x_mas=}')
