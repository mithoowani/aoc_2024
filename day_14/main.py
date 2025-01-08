import re

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


# grid size (x, y) = (number of cols, number of rows)
# set to (11, 7) if using test input
dimensions = (101, 103)
num_seconds = 100

with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()
bots = parse_input(REAL_INPUT)

# bots = parse_input(TEST_INPUT)

for bot in bots:
	bot.x = (bot.x + num_seconds * bot.velocity[0]) % dimensions[0]
	bot.y = (bot.y + num_seconds * bot.velocity[1]) % dimensions[1]

quadrants = [0] * 4

for bot in bots:
	if bot.x < dimensions[0] // 2 and bot.y < dimensions[1] // 2:
		quadrants[0] += 1
	elif bot.x > dimensions[0] // 2 and bot.y < dimensions[1] // 2:
		quadrants[1] += 1
	elif bot.x < dimensions[0] // 2 and bot.y > dimensions[1] // 2:
		quadrants[2] += 1
	elif bot.x > dimensions[0] // 2 and bot.y > dimensions[1] // 2:
		quadrants[3] += 1

answer = 1

for quadrant in quadrants:
	answer *= quadrant

print(answer)
