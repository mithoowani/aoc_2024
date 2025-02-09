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

starting_A = A
pointer = 0
output = []

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

print(f'Part A: {",".join([str(num) for num in output])}')
