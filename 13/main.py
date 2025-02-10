import re
import numpy as np
from pprint import pprint

TEST_INPUT_1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def parse_input(puzzle_input):
	"""
	Parses puzzle input into a list of claw machines
	Each claw machine is a list, e.g. : Button A: X+94[0], Y+34[1]
								 		Button B: X+22[2], Y+67[3]
										Prize: X=8400[4], Y=5400[5]
	"""
	claw_machines = []
	str_to_match = """\s|=|\+|,"""
	nums_only = [word for word in re.split(str_to_match, puzzle_input) if word.isnumeric()]
	machine = []
	for i, num in enumerate(nums_only):
		machine.append(int(num))
		if (i + 1) % 6 == 0:
			claw_machines.append(machine)
			machine = []
	return claw_machines


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()
all_machines = parse_input(REAL_INPUT)

total_a = 0
total_b = 0

for machine in all_machines:

	# System of linear equations, e.g.
	# a(94) + b(22) = 8400
	# a(34) + b(67) = 5400
	A = [[machine[0], machine[2]], [machine[1], machine[3]]]
	B_part_a = np.array([machine[4], machine[5]])
	B_part_b = np.array([machine[4] + 10000000000000, machine[5] + 10000000000000])

	# rounding to 3 decimals is arbitrary but avoids floating point errors
	solution_a = np.round(np.linalg.solve(A, B_part_a), decimals=3)
	solution_b = np.round(np.linalg.solve(A, B_part_b), decimals=3)

	# if a and b in the linear equations above are integers, then the prize can be won
	if np.all(solution_a % 1 == 0):
		total_a += 3 * solution_a[0] + solution_a[1]

	if np.all(solution_b % 1 == 0):
		total_b += 3 * solution_b[0] + solution_b[1]

print(f'Part A: {int(total_a)}')
print(f'Part B: {int(total_b)}')
