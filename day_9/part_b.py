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


"""
Files could be a list of File dataclasses
FreeSpaces could be a list; where the index represents the start position and value represents size
"""


def parse_input(puzzle_input):
	file_num = 0
	index = 0
	all_files = []
	all_free_spaces = []

	# populate the filesystem
	for i, size in enumerate(puzzle_input):
		size = int(size)

		# representing a file
		if i % 2 == 0:
			file = File(name=file_num, size=size)
			all_files.append(file)
			for j in range(file.size):
				all_free_spaces.append(None)
			file_num += 1
			index += size

		# representing free space
		else:
			if size > 0:
				all_free_spaces.append(size)
			index += size

	return all_files, all_free_spaces


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


# def free_up_space(fs, k):
# 	if k == len(fs) - 1 and type(fs[k - 1]) is FreeSpace:
# 		fs[k - 1].size += fs[k].size
# 		del fs[k]
# 		k -= 1
#
# 	elif k == len(fs) - 1 and type(fs[k - 1]) is File:
# 		fs[k] = FreeSpace(size=fs[k].size)
#
# 	elif type(fs[k - 1]) is File and type(fs[k + 1]) is File:
# 		fs[k] = FreeSpace(size=fs[k].size)
#
# 	elif type(fs[k - 1]) is File and type(fs[k + 1]) is FreeSpace:
# 		fs[k + 1].size += fs[k].size
# 		del fs[k]
# 		k -= 1
#
# 	elif type(fs[k - 1]) is FreeSpace and type(fs[k + 1]) is File:
# 		fs[k - 1].size += fs[k].size
# 		del fs[k]
# 		k -= 1
#
# 	elif type(fs[k - 1]) is FreeSpace and type(fs[k + 1]) is FreeSpace:
# 		fs[k - 1].size += fs[k].size + fs[k + 1].size
# 		del fs[k + 1]  # have to delete the rightmost element first
# 		del fs[k]
# 		k -= 2
#
# 	return fs, k


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

files, free_spaces = parse_input(TEST_INPUT)

pprint(free_spaces)

"""
Could probably re-write this with two separate lists;
one a list of files (file_num, start_index, size)
and another list of free spaces (start_index, size) 
Similar to the original implementation

Iterate through files first, in reverse order
Then iterate through free spaces UP TO start index of the file in question to find a match

"""

# j = len(filesystem) - 1
#
# while not all(item.checked for item in filesystem if type(item) is File):
#
# 	# iterate through files first
# 	while j > 0 and (type(filesystem[j]) is not File or filesystem[j].checked):
# 		j -= 1
#
# 	filesystem[j].checked = True
#
# 	for i, free_space in enumerate(filesystem[:j]):
#
# 		if type(filesystem[i]) is FreeSpace:
#
# 			if filesystem[i].size == filesystem[j].size:
# 				filesystem[i], filesystem[j] = filesystem[j], filesystem[i]
# 				break
#
# 			elif filesystem[i].size > filesystem[j].size:
# 				filesystem[i].size -= filesystem[j].size
# 				filesystem.insert(i, filesystem[j])
# 				filesystem[j + 1] = FreeSpace(size=filesystem[i].size)
# 				break


# checksum = 0
# index = 0
# for item in filesystem:
# 	if type(item) is File:
# 		for position in range(index, index + item.size):
# 			checksum += item.name * position
# 	index += item.size
#
# print(checksum)


