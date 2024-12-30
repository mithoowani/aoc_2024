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


"""
TODO: There's got to be a cleaner way to write this 
		Perhaps with None at the end of the filesystem to eliminate the first two conditions
		Can the deletions be eliminated? That's what's forcing the pointer k to be adjusted every time
		Probably deletions and insertions are what's slowing down the algorithm
		Alternatively, consider implementing this is a linked list (or deque) in which case insertions and deletions
		would be O(1)
		
		
		Is freeing up space at the file even necessary???
		You don't need any of this code!!! No need to concatenate free space to the right of the file
		Because NOTHING ever moves into it!!!
"""


def free_up_space(fs, k):
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

"""
Could probably re-write this with two separate lists;
one a list of files (file_num, start_index, size)
and another list of free spaces (start_index, size) 
Similar to the original implementation

Iterate through files first, in reverse order
Then iterate through free spaces UP TO start index of the file in question to find a match

"""

j = len(filesystem) - 1

while not all(item.checked for item in filesystem if type(item) is File):

	# iterate through files first
	while j > 0 and (type(filesystem[j]) is not File or filesystem[j].checked):
		j -= 1

	filesystem[j].checked = True

	for i, free_space in enumerate(filesystem[:j]):

		if type(filesystem[i]) is FreeSpace:

			if filesystem[i].size == filesystem[j].size:
				filesystem[i], filesystem[j] = filesystem[j], filesystem[i]
				break

			elif filesystem[i].size > filesystem[j].size:
				filesystem[i].size -= filesystem[j].size
				filesystem.insert(i, filesystem[j])
				filesystem[j+1] = FreeSpace(size=filesystem[i].size)
				break

	# if file_moved:
	# 	filesystem, j = free_up_space(filesystem, j)
	#
	# elif file_inserted:
	# 	filesystem, j = free_up_space(filesystem, j + 1)

# pprint(filesystem)

checksum = 0
index = 0
for item in filesystem:
	if type(item) is File:
		for position in range(index, index + item.size):
			checksum += item.name * position
	index += item.size

print(checksum)

# for i, file in enumerate(filesystem[::-1]):
# 	file_moved = False
# 	forward_index = -1 * (i + 1)
#
# 	if type(file) is File and not file.checked:
# 		file.checked = True
#
# 		for j, free_space in enumerate(filesystem):
# 			if type(free_space) is FreeSpace:
# 				if free_space.size == file.size:
# 					filesystem[j] = file
# 					file_moved = True
# 					break
#
# 				elif free_space.size > file.size:
# 					filesystem[j].size -= file.size
# 					filesystem.insert(j, file)
# 					file_moved = True
# 					break
#
#
# 	# I think the issue is modifying the list as it's being iterated on
# 	if file_moved:
# 		filesystem = free_up_space(filesystem, forward_index)
# 		pass
#
# pprint(filesystem)


#
# for file in files[::-1]:
# 	free_space_to_delete = None
# 	for i, free_space in enumerate(spaces):
# 		if free_space.size >= file.size:
# 			file.start_index = free_space.start_index
# 			free_space.size -= file.size
# 			free_space.start_index += file.size
# 			if free_space.size == 0:
# 				free_space_to_delete = i
# 			break
# 	if free_space_to_delete is not None:
# 		del spaces[free_space_to_delete]
#
# pprint(sorted(files, key=lambda x: x.start_index))
# pprint(spaces)
#
# checksum = 0
# for file in files:
# 	for position in range(file.start_index, file.start_index+file.size):
# 		checksum += file.name * position
# print(checksum)
