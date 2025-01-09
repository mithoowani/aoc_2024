import re
import numpy as np

TEST_INPUT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


class Robot:
	def __init__(self, start_pos: tuple, velocity: tuple):
		self.start_pos = start_pos
		self.velocity = velocity
		self.x: int = start_pos[0]
		self.y: int = start_pos[1]

	def __repr__(self):
		return f"({self.x}, {self.y})"

	def __str__(self):
		return self.__repr__()


def parse_input(puzzle_input):
	robots = []
	re_string = r"-?\d+"
	for robot in puzzle_input.split('\n'):
		digits = re.findall(re_string, robot)
		digits = [int(digit) for digit in digits]
		robots.append(Robot(start_pos=(digits[0], digits[1]),
							velocity=(digits[2], digits[3])))
	return robots


def part_a(bots_) -> int:
	"""
	Part A solution
	:param bots_: a list of Robot objects
	:return: solution to Part a
	"""

	# Determine the final position of all bots
	for bot in bots_:
		bot.x = (bot.x + num_seconds * bot.velocity[0]) % dimensions[0]
		bot.y = (bot.y + num_seconds * bot.velocity[1]) % dimensions[1]

	quadrants = [0] * 4

	for bot in bots_:
		if bot.x < dimensions[0] // 2 and bot.y < dimensions[1] // 2:
			quadrants[0] += 1  # upper left
		elif bot.x > dimensions[0] // 2 and bot.y < dimensions[1] // 2:
			quadrants[1] += 1  # upper right
		elif bot.x < dimensions[0] // 2 and bot.y > dimensions[1] // 2:
			quadrants[2] += 1  # lower left
		elif bot.x > dimensions[0] // 2 and bot.y > dimensions[1] // 2:
			quadrants[3] += 1  # lower right

	answer = 1

	for quadrant in quadrants:
		answer *= quadrant

	return answer


def print_grid(second, grid_):
	"""
	Prints the grid at a given second
	:param second: number of seconds elapsed (int)
	:param grid_: grid (np.array)
	:return: None
	"""
	print(f'Part B: {second}')
	for line in grid_:
		string_line = ''.join(list(line))
		print(string_line)


def part_b(bots_, dim):
	"""
	Part B solution
	:param bots_: a list of Robot objects
	:param dim: grid size (x, y) = (number of cols, number of rows)
	:return: None
	"""
	for second in range(10_000):
		grid_ = np.full((dim[1], dim[0]), '.')
		for bot in bots_:
			bot.x = (bot.start_pos[0] + second * bot.velocity[0]) % dimensions[0]
			bot.y = (bot.start_pos[1] + second * bot.velocity[1]) % dimensions[1]
			grid_[bot.y, bot.x] = '#'

		# Making an assumption that the christmas tree has to have a long line of robots
		# next to one another
		for line in grid_:
			string_line = ''.join(list(line))
			if '#############' in string_line:
				print_grid(second, grid_)
				return


# grid size (x, y) = (number of cols, number of rows)
# manually set to (11, 7) if using test input
dimensions = (101, 103)
num_seconds = 100

# Test input
# bots = parse_input(TEST_INPUT)

# Real input
with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

bots = parse_input(REAL_INPUT)

# Part A
ans = part_a(bots)
print(f'Part A: {ans}')

# Part B
part_b(bots, dimensions)
