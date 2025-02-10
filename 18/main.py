from dataclasses import dataclass
from collections import deque

TEST_INPUT = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


@dataclass(frozen=True, order=True)
class Location:
	row: int
	col: int


class Graph:
	"""
	Represents a 2D grid; inspired by Redblobgames article
	Note that there is no Node object, instead this is basically a collection of helper functions for a 2D numpy array
	"""

	def __init__(self, walls: list[tuple], height, width):
		self.height = height
		self.width = width
		self.walls = walls

	def in_bounds(self, loc: Location):
		return 0 <= loc.row < self.height and 0 <= loc.col < self.width

	def passable(self, loc: Location):
		return (loc.row, loc.col) not in self.walls

	def neighbours(self, loc: Location):
		"""Returns neighbours of the current location; neighbours are 1 space up, down, left or right
		from the current location"""

		row, col = loc.row, loc.col
		neighbours = []

		# no neighbours because location is invalid
		if not self.in_bounds(loc) or not self.passable(loc):
			return []

		for neighbour in [Location(row + 1, col), Location(row - 1, col),
						  Location(row, col - 1), Location(row, col + 1)]:
			if self.in_bounds(neighbour) and self.passable(neighbour):
				neighbours.append(neighbour)

		return neighbours


def parse_input(puzzle_input):
	walls = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in puzzle_input.split('\n')]
	return walls


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

HEIGHT, WIDTH = 71, 71
walls = parse_input(REAL_INPUT)


def part_A():
	"""BFS using graph with first 1024 walls"""
	start = Location(row=0, col=0)
	end = Location(row=HEIGHT - 1, col=WIDTH - 1)

	frontier = deque([start])
	came_from = {start: None}

	graph = Graph(walls[:1024], HEIGHT, WIDTH)
	while frontier:
		current = frontier.popleft()

		if current == end:
			break

		for neighbour in graph.neighbours(current):
			if neighbour not in came_from:
				frontier.append(neighbour)
				came_from[neighbour] = current

	length_of_path = 0
	current = end
	while current != start:
		current = came_from[current]
		length_of_path += 1

	return length_of_path


def part_B():
	"""Inefficient but works... repeatedly does a BFS search until the path is blocked"""
	for num_bytes in range(1024, len(walls)):
		start = Location(row=0, col=0)
		end = Location(row=HEIGHT - 1, col=WIDTH - 1)

		frontier = deque([start])
		came_from = {start: None}

		graph = Graph(walls[:num_bytes], HEIGHT, WIDTH)
		while frontier:
			current = frontier.popleft()

			if current == end:
				break

			for neighbour in graph.neighbours(current):
				if neighbour not in came_from:
					frontier.append(neighbour)
					came_from[neighbour] = current

		if current != end:
			return num_bytes


print(f'part A: {part_A()}')
last_wall = part_B()
print(f'part B: {walls[last_wall - 1][1], walls[last_wall - 1][0]}')
