def parse_input(puzzle):
	"""Extracts the machine instructions from puzzle input"""
	lines = puzzle.split('\n\n')
	program_ = [int(num) for num in lines[1].removeprefix('Program: ').split(',')]
	return program_


def return_output(A):
	"""Translating the machine instructions into a more digestable format"""
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


def search_paths(index=0, sequence=None):
	"""
	Analysis of the instruction set reveals that to produce a 16 character output, the starting value of register A
	A lies between 8^15 and 8^16

	Pattern recognition shows that the approach is to manipulate one octal of the A register at a time;
	the most significant octal in A manipulates the least significant digit of the output

	The approach is to do a DFS of A possibilities, expressed in octal form, starting from 8^15
	Manipulate one digit at a time starting with the most significant
	At each step, check if the correct digit was found in the output; and if so, continue with the search
	"""
	if sequence is None:
		sequence = [0] * 16

	if index == 16:
		octal_string = '0o' + ''.join([str(num) for num in sequence])
		out = return_output(int(octal_string, 8))
		if out == INSTRUCTIONS:
			print(octal_string)
			print(int(octal_string, 8))
			print()

	else:
		for possibility in range(8):
			new_sequence = sequence[:]
			new_sequence[index] = possibility
			out = return_output(int('0o' + ''.join([str(num) for num in new_sequence]), 8))
			if len(out) == 16 and out[15 - index] == INSTRUCTIONS[15 - index]:
				search_paths(index + 1, new_sequence)


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

INSTRUCTIONS = parse_input(REAL_INPUT)

search_paths()
