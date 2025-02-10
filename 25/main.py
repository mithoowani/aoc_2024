import numpy as np
from pprint import pprint

TEST_INPUT = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


def parse_input(puzzle_input: str):
	"""Converts puzzle input (string) into np array"""
	locks_ = []  # top row filled with #
	keys_ = []  # bottom row filled with #

	for lock_key in puzzle_input.split('\n\n'):
		block_list = []
		for line in lock_key.split('\n'):
			block_list.append(list(line))
		lock_key_array = np.array(block_list)
		num = np.count_nonzero(lock_key_array == '#', axis=0) - 1
		if lock_key_array[0][0] == '#':  # lock
			locks_.append(num)
		else:
			keys_.append(num)

	return locks_, keys_


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

locks, keys = parse_input(REAL_INPUT)

part_A = 0
for key in keys:
	for lock in locks:
		if np.all(key + lock <= 5):
			part_A += 1
print(f'{part_A=}')
