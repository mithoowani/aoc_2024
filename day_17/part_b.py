from pprint import pprint
from collections import defaultdict, deque

# Instructions: 2,4,1,1,7,5,0,3,1,4,4,0,5,5,3,0
INSTRUCTIONS = [2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0]


def return_output(A):
	output = []

	while A > 0:
		B = A % 8
		B = B ^ 1
		C = int(A / 2 ** B)
		B = B ^ 4
		B = B ^ C
		output.append(B % 8)
		A = int(A / 8)

	return output


def get_possible_octals():
	possibilities = defaultdict(list)

	for index in range(16):
		octal_sequence = list('1000000000000000')  # 8^15
		for possibility in range(0, 8):
			if index == 0 and possibility == 0:
				continue
			octal_sequence[index] = str(possibility)
			octal_string = '0o' + ''.join(octal_sequence)
			octal = int(octal_string, 8)
			output = return_output(octal)
			# print(index, possibility, output)
			if len(output) == 16 and output[15 - index] == INSTRUCTIONS[15 - index]:
				possibilities[index].append(possibility)

	for index in range(16):
		if possibilities.get(index) is None:
			possibilities[index].extend(list(range(8)))

	return possibilities


# def search_paths(index=0, sequence=None):
# 	global all_combinations
#
# 	if sequence is None:
# 		sequence = []
# 	if index == 16:
# 		all_combinations.append(sequence)
# 	else:
# 		for possibility in all_paths[index]:
# 			new_sequence = sequence[:]
# 			new_sequence.append(possibility)
# 			search_paths(index + 1, new_sequence)


def search_paths(index=0, sequence=None):
	if sequence is None:
		sequence = [0] * 16
	if index == 16:
		octal_string = '0o' + ''.join([str(num) for num in sequence])
		out = return_output(int(octal_string, 8))
		if out == INSTRUCTIONS:
			print(octal_string)
			print(int(octal_string, 8))
			print(out)
			print()

	else:
		for possibility in range(8):
			new_sequence = sequence[:]
			new_sequence[index] = possibility
			out = return_output(int('0o' + ''.join([str(num) for num in new_sequence]), 8))
			if len(out) == 16 and out[15 - index] == INSTRUCTIONS[15 - index]:
				search_paths(index + 1, new_sequence)


# all_combinations = []
# all_paths = get_possible_octals()
# pprint(all_paths)

search_paths()
# pprint(all_combinations)
#
# for combination in all_combinations:
# 	octal_string = '0o' + ''.join([str(num) for num in combination])
# 	octal = int(octal_string, 8)
# 	output = return_output(octal)
# 	# print(output)
# 	if output == INSTRUCTIONS:
# 		print(octal)
# 		break

lowest = 0b1000000000000000000000000000000000000000000000  # 8^15 = 2^45 (46 characters long)
highest = 0b1000000000000000000000000000000000000000000000000  # 8^16 = 2^48 (49 characters long)

##  BINARY exercise ##
# binary_list = list('0b100000000000000000000000000000000000000000000000')
# new_binary_list = binary_list[:]
#
# print_output(highest)
# print()
# for i, item in enumerate(binary_list[2:]):
# 	# new_binary_list = binary_list[:]
# 	new_binary_list[i + 2] = '1'
# 	print(''.join(new_binary_list))
# 	print_output(int(''.join(new_binary_list), 2))
# 	print()

## OCTAL exercise ##
# lowest_octal = 0o1000000000000000  # 8^15
# highest_octal = 0o10000000000000000 # 8^16
#
# octal_list = list('0o1000000000000000')
# new_octal_list = octal_list[:]
#
# for i, item in enumerate(octal_list[2:]):
# 	new_octal_list[i + 2] = '1'
# 	print(''.join(new_octal_list))
# 	print_output(int(''.join(new_octal_list), 8))
# 	print()


"""
Start with a 48 character binary string
0b0000000000000000000000000000000000000000000000

Turn into a string
Manipulate 1 bit at a time, starting right most (this changes ouput from R to L)
If the correct digit is found; then search further with backtracking (DFS)


"""

# Manipulating octal numbers
# print(return_output(0o1000000000000000))
# print(return_output(0o1000010000000000))
# print(return_output(0o1000020000000000))
# print(return_output(0o1000030000000000))
# print(return_output(0o5601570000000000)) # pick this one; 5 is equivalent to 101 in binary
# print(return_output(0o5610570000000000))
# print(return_output(0o5600532700000000))  # position 7 is not a 4 as predicted; it's a 7
# print(return_output(0o5611570000000000))
# print()

# Manipulating binary numbers
#
# First three bits (index 0-2) represent last digit
# print_output(0b100000000000000000000000000000000000000000000000) # 100
# print_output(0b111000000000000000000000000000000000000000000000) # 111
# print_output(0b101000000000000000000000000000000000000000000000) # 101 proceed with this one
# print_output(0b110000000000000000000000000000000000000000000000) # 110
# print_output(0b010000000000000000000000000000000000000000000000) # 010
# print_output(0b001000000000000000000000000000000000000000000000) # 001
# print_output(0b011000000000000000000000000000000000000000000000) # 011

# Index 2-4 manipulate second last digit
# print_output(0b101110000000000000000000000000000000000000000000) # 111 candidate proceed with this one
# print_output(0b101010000000000000000000000000000000000000000000) # 101
# print_output(0b101100000000000000000000000000000000000000000000) # 011
# print_output(0b101000000000000000000000000000000000000000000000) # 100
# print_output(0b100110000000000000000000000000000000000000000000) # 110
# print_output(0b100010000000000000000000000000000000000000000000) # 001 candidate
# print_output(0b100000000000000000000000000000000000000000000000) # 000 candidate
# print_output(0b100100000000000000000000000000000000000000000000) # 010
