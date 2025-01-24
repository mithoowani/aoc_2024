import re

TEST_INPUT = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


def parse_input(puzzle):
	lines = puzzle.split('\n\n')
	re_string = r'\d+'
	reg_A, reg_B, reg_C = re.findall(re_string, lines[0])
	program_ = [int(num) for num in lines[1].removeprefix('Program: ').split(',')]
	return int(reg_A), int(reg_B), int(reg_C), program_


def adv(operand):
	global A
	numerator = A
	denominator = 2 ** COMBO_OPERANDS[operand]
	A = int(numerator / denominator)


def bdv(operand):
	global A, B
	numerator = A
	denominator = 2 ** COMBO_OPERANDS[operand]
	B = int(numerator / denominator)


def cdv(operand):
	global A, C
	numerator = A
	denominator = 2 ** COMBO_OPERANDS[operand]
	C = int(numerator / denominator)


def bxl(operand):
	global B
	B = B ^ operand


def bst(operand):
	global B
	B = COMBO_OPERANDS[operand] % 8


def jnz(operand):
	global pointer
	pointer = operand


def bxc(operand):
	global B
	B = B ^ C


def out(operand):
	global output
	output.append(COMBO_OPERANDS[operand] % 8)


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

A, B, C, program = parse_input(REAL_INPUT)

INSTRUCTIONS = {
	0: adv,
	1: bxl,
	2: bst,
	3: jnz,
	4: bxc,
	5: out,
	6: bdv,
	7: cdv
}

# 1    2    3    4     5     6     7     8     9     10    11    12    13    14    15    16
# 2^1, 2^4, 2^7, 2^10, 2^13, 2^16, 2^19, 2^22, 2^25, 2^28, 2^31, 2^34, 2^37, 2^40, 2^43, 2^46
# 2, 16, 128, 1024, 8192, 65546, in forward direction

for A in range(8**16-200, 8**16, 1):

	starting_A = A
	pointer = 0
	output = []
	B, C = 0, 0

	while pointer < len(program):

		# Have to re-initialize because A, B, C is updated regularly
		COMBO_OPERANDS = {
			0: 0,
			1: 1,
			2: 2,
			3: 3,
			4: A,
			5: B,
			6: C
		}

		instruction = INSTRUCTIONS[program[pointer]]
		if instruction is jnz and A > 0:
			instruction(program[pointer + 1])  # do not advance pointer further
		elif instruction is jnz and A == 0:
			pointer += 2  # do nothing
		else:
			instruction(program[pointer + 1])
			pointer += 2

	print(starting_A, bin(starting_A), output)

	# output = ','.join([str(digit) for digit in output])
	# if output == [2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 0, 5, 5, 3, 0]:
	# 	print(A)
	# 	break
