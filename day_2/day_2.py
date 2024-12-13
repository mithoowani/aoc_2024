import numpy as np

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open('input.txt', 'r') as f:
	INPUT = f.read()


def parse_input(puzzle_input: str) -> list:
	# returns a list of np arrays; one for each report
	array = puzzle_input.split('\n')
	array_lists = []
	for report in array:
		array_lists.append(np.array(report.split(), dtype=int))
	return array_lists


def return_diffs_row(row: np.array) -> np.array:
	row_diffs = []
	for i in range(row.shape[0] - 1):
		row_diffs.append(row[i] - row[i + 1])
	return np.array(row_diffs)


def return_diffs(puzzle_input: list) -> np.array:
	diffs = []
	for i, row in enumerate(puzzle_input):
		row_diffs = np.zeros(row.shape[0], dtype=int)
		for j in range(row.shape[0] - 1):
			row_diffs[j] = row[j] - row[j + 1]
		diffs.append(row_diffs[:-1])
	return diffs


def validate_diffs_row(row: np.array) -> bool:
	condition_1 = row > 0
	condition_2 = row < 0
	condition_3 = (np.abs(row) > 0) & (np.abs(row) < 4)

	# All values positive and steps between 1-3
	conditions_1_3 = np.all((condition_1 & condition_3))

	# All values negative and steps between 1-3
	conditions_2_3 = np.all((condition_2 & condition_3))

	all_conditions_met = np.vstack((conditions_1_3, conditions_2_3))

	return np.any(all_conditions_met)


def validate_diffs_partb(row: np.array) -> bool:
	diffs = return_diffs_row(row)
	if validate_diffs_row(diffs):
		return True

	else:
		conditions_met = []
		for i in range(row.shape[0]):
			row_deleted = np.delete(row, i)
			diffs = return_diffs_row(row_deleted)
			conditions_met.append(validate_diffs_row(diffs))
		conditions_met = np.array(conditions_met)
		return np.any(conditions_met)


array = parse_input(INPUT)

# PART A
count_safe = 0
diffs = return_diffs(array)
for row in diffs:
	if validate_diffs_row(row):
		count_safe += 1
print(count_safe)

# PART B
count_safe_partb = 0
for row in array:
	if validate_diffs_partb(row):
		count_safe_partb += 1
print(count_safe_partb)
