from dataclasses import dataclass

TEST_INPUT = "2333133121414131402"
TEST_INPUT_2 = "1313165"
TEST_INPUT_3 = "9953877292941"
TEST_INPUT_4 = "0112233"


@dataclass
class File:
	"""
	Simple class representing a file
	"""
	name: int
	start_index: int
	size: int


@dataclass
class FreeSpace:
	"""
	Simple class representing a block of free space (one or more free spaces)
	"""
	size: int


def parse_input(puzzle_input):
	"""
	Parses puzzle input
	all_files is a list of File dataclasses
	all_free_spacec is a list; index represents the start position and value represents size
	"""
	file_num = 0
	index = 0
	all_files = []
	all_free_spaces = []

	# populate the filesystem
	for i, size in enumerate(puzzle_input):
		size = int(size)

		# representing a file
		if i % 2 == 0:
			if size > 0:
				file = File(name=file_num, size=size, start_index=index)
				all_files.append(file)
				for j in range(file.size):
					all_free_spaces.append(0)
				index += size
			file_num += 1

		# representing free space
		else:
			if size > 0:
				all_free_spaces.append(size)
				for j in range(size - 1):
					all_free_spaces.append(0)
				index += size

	return all_files, all_free_spaces


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

files, free_spaces = parse_input(REAL_INPUT)

for file in reversed(files):

	# identifies the first free space with a large enough size to accommodate the file
	g = (i for i, val in enumerate(free_spaces[:file.start_index]) if val >= file.size)
	try:
		free_space_index = next(g)
	except StopIteration:
		free_space_index = None

	# if a compatible free space was found
	if free_space_index:

		if free_spaces[free_space_index] == file.size:
			free_spaces[free_space_index] = 0
			file.start_index = free_space_index

		elif free_spaces[free_space_index] > file.size:
			file.start_index = free_space_index
			free_spaces[free_space_index + file.size] = free_spaces[free_space_index] - file.size
			free_spaces[free_space_index] = 0

checksum = 0
for file in files:
	for i in range(file.start_index, file.start_index + file.size):
		checksum += file.name * i
print(f'Part B: {checksum}')
