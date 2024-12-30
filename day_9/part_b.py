from dataclasses import dataclass
from pprint import pprint
from copy import copy
from collections import deque

TEST_INPUT = "2333133121414131402"


@dataclass
class File:
	"""
	Simple class representing a file
	"""
	name: int
	size: int
	checked: bool = False


@dataclass
class FreeSpace:
	"""
	Simple class representing a block of free space (one or more free spaces)
	"""
	size: int


def parse_input(puzzle_input):
	"""
	Parses puzzle input into a file system (list) with file and free space blocks
	"""
	file_num = 0
	index = 0
	filesystem_ = []

	# populate the filesystem
	for i, size in enumerate(puzzle_input):
		size = int(size)

		# representing a file
		if i % 2 == 0:
			file = File(name=file_num, size=size)
			filesystem_.append(file)
			file_num += 1
			index += size

		# representing free space
		else:
			if size > 0:
				filesystem_.append(FreeSpace(size=size))
			index += size

	return filesystem_


def free_up_space(fs, k):
	"""
	This ended up not being necesary (and is unused)
	Concatenates free space to the right of the file that was moved to create contiguous free space blocks
	"""
	if k == len(fs) - 1 and type(fs[k - 1]) is FreeSpace:
		fs[k - 1].size += fs[k].size
		del fs[k]
		k -= 1

	elif k == len(fs) - 1 and type(fs[k - 1]) is File:
		fs[k] = FreeSpace(size=fs[k].size)

	elif type(fs[k - 1]) is File and type(fs[k + 1]) is File:
		fs[k] = FreeSpace(size=fs[k].size)

	elif type(fs[k - 1]) is File and type(fs[k + 1]) is FreeSpace:
		fs[k + 1].size += fs[k].size
		del fs[k]
		k -= 1

	elif type(fs[k - 1]) is FreeSpace and type(fs[k + 1]) is File:
		fs[k - 1].size += fs[k].size
		del fs[k]
		k -= 1

	elif type(fs[k - 1]) is FreeSpace and type(fs[k + 1]) is FreeSpace:
		fs[k - 1].size += fs[k].size + fs[k + 1].size
		del fs[k + 1]  # have to delete the rightmost element first
		del fs[k]
		k -= 2

	return fs, k


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

filesystem = parse_input(REAL_INPUT)

j = len(filesystem) - 1

while not all(item.checked for item in filesystem if type(item) is File):

	# first iteration through filesystem is to identify unchecked files
	while j > 0 and (type(filesystem[j]) is not File or filesystem[j].checked):
		j -= 1

	filesystem[j].checked = True

	# second iteration through filesystem identifies a free space that is large enough to accomodate the file
	for i, free_space in enumerate(filesystem[:j]):

		if type(filesystem[i]) is FreeSpace:

			if filesystem[i].size == filesystem[j].size:
				filesystem[i], filesystem[j] = filesystem[j], filesystem[i]
				break

			elif filesystem[i].size > filesystem[j].size:
				filesystem[i].size -= filesystem[j].size
				filesystem.insert(i, filesystem[j])
				filesystem[j + 1] = FreeSpace(size=filesystem[i].size)
				break

checksum = 0
index = 0
for item in filesystem:
	if type(item) is File:
		for position in range(index, index + item.size):
			checksum += item.name * position
	index += item.size

print(f'Part B: {checksum}')
