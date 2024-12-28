import numpy as np

TEST_INPUT = "2333133121414131402"


def parse_input(puzzle_input):
	# create np array with appropriate length representing the file system
	filesystem_size = 0
	for digit in puzzle_input:
		filesystem_size += int(digit)
	filesystem = np.empty(filesystem_size)

	# populate the filesystem
	index = 0
	file_num = 0
	for i, size in enumerate(puzzle_input):
		size = int(size)

		# representing a file
		if i % 2 == 0:
			for position in range(index, index + size):
				filesystem[position] = file_num
				index += 1
			file_num += 1

		# representing free space
		else:
			for position in range(index, index + size):
				filesystem[position] = np.nan
				index += 1

	return filesystem


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

array = parse_input(REAL_INPUT)

# two pointers, one on either end of the array
i, j = 0, len(array) - 1

while True:
	# advance left pointer until an empty space is found
	while not np.isnan(array[i]):
		i += 1

	# advance right pointer until a file is found
	while np.isnan(array[j]):
		j -= 1

	# if pointers cross each other, then the routine is done
	if i > j:
		break

	# swap empty space with file
	array[i], array[j] = array[j], np.nan

checksum = 0
for i, file_num in enumerate(array):
	if not np.isnan(file_num):
		checksum += i * file_num

print(f'Part A: {int(checksum)}')
