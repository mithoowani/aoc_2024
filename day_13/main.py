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

# pprint(all_machines)

total = 0
part_b = True

for machine in all_machines:
	A = [[machine[0], machine[2]], [machine[1], machine[3]]]

	if part_b:
		B = np.array([machine[4] + 10000000000000, machine[5] + 10000000000000]).astype('float64')
	else:
		B = np.array([machine[4], machine[5]]).astype('float64')

	solution = np.round(np.linalg.solve(A, B), decimals=3)
	print(solution[0], solution[1])
	# print(solution)

	if np.all(solution % 1 == 0):
		total += 3 * solution[0] + solution[1]

print(f'Solution: {int(total)}')

#87847634286897
#3 decimals 87596249540359  # Correct, but not really sure why 3 decimals were needed. Look up solutions
