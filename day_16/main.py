"""
Graph/location data structure and Dijkstra algorithms inspired by:
https://www.redblobgames.com/pathfinding/a-star/introduction.html
"""

from collections import defaultdict, deque
from queue import PriorityQueue
from dataclasses import dataclass
import numpy as np

TEST_INPUT_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

TEST_INPUT_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


# Frozen allows hashing of the resulting objects; order allows them to be used in a priority queue
@dataclass(frozen=True, order=True)
class Location:
	row: int
	col: int
	dir: str  # direction N, S, E, W


class Graph:
	"""
	Represents a 2D grid; inspired by Redblobgames article
	Note that there is no Node object, instead this is basically a collection of helper functions for a 2D numpy array
	"""

	def __init__(self, graph: np.array):
		self.graph = graph
		self.height = graph.shape[0]
		self.width = graph.shape[1]
		self.walls = list(zip(np.where(graph == '#')[0], np.where(graph == '#')[1]))

	def in_bounds(self, loc: Location):
		return 0 <= loc.row < self.height and 0 <= loc.col < self.width

	def passable(self, loc: Location):
		return (loc.row, loc.col) not in self.walls

	def neighbours(self, loc: Location):
		"""Returns neighbours of the current location; neighbours are a left or right turn in place or advance
		by 1 tile in the current direction"""
		row, col, dir = loc.row, loc.col, loc.dir
		neighbours = []

		# no neighbours because location is invalid
		if not self.in_bounds(loc) or not self.passable(loc):
			return []

		match dir:
			case 'E':
				neighbours.extend([Location(row, col, 'S'),  # right turn
								   Location(row, col, 'N')])  # left turn
				advance = Location(row, col + 1, 'E')  # advance by 1
				if self.in_bounds(advance) and self.passable(advance):
					neighbours.append(advance)

			case 'S':
				neighbours.extend([Location(row, col, 'W'),  # right turn
								   Location(row, col, 'E')])  # left turn
				advance = Location(row + 1, col, 'S')  # advance by 1
				if self.in_bounds(advance) and self.passable(advance):
					neighbours.append(advance)

			case 'W':
				neighbours.extend([Location(row, col, 'N'),  # right turn
								   Location(row, col, 'S')])  # left turn
				advance = Location(row, col - 1, 'W')  # advance by 1
				if self.in_bounds(advance) and self.passable(advance):
					neighbours.append(advance)

			case 'N':
				neighbours.extend([Location(row, col, 'E'),  # right turn
								   Location(row, col, 'W')])  # left turn
				advance = Location(row - 1, col, 'N')  # advance by 1
				if self.in_bounds(advance) and self.passable(advance):
					neighbours.append(advance)

		return neighbours

	@staticmethod
	def cost(loc1: Location, loc2: Location):
		"""Returns cost associated with moving from loc1 to loc2;
		cost is 1000 for a turn, or 1 to advance by 1 square"""
		if (loc1.row, loc1.col) == (loc2.row, loc2.col) and loc1.dir != loc2.dir:
			return 1000
		elif loc1.dir == loc2.dir and abs((loc1.row - loc2.row)) + abs((loc1.col - loc2.col)) == 1:
			return 1
		else:
			raise Exception('Not neighbours')

	def __str__(self):
		return f'{self.graph}'


def parse_input(puzzle_input: str):
	"""Converts puzzle input (string) into np array"""
	maze_lists = []
	for line in puzzle_input.split('\n'):
		maze_lists.append(list(line))
	maze_array = np.array(maze_lists)
	return maze_array


def get_start_end_locations(graph_: Graph):
	"""Returns location of the start and end positions as Location objects"""
	start_loc = int(np.where(graph_.graph == 'S')[0][0]), int(np.where(graph.graph == 'S')[1][0])
	end_loc = int(np.where(graph_.graph == 'E')[0][0]), int(np.where(graph.graph == 'E')[1][0])

	# hard coded --
	start = Location(start_loc[0], start_loc[1], 'E')
	end = Location(end_loc[0], end_loc[1], dir='E')

	return start, end


def dijkstra_shortest_path(start, end, graph_):
	# Frontier is a priority queue, so that it remains sorted by priority (cost)
	# Entries in the priority queue are in the form (cost, location)
	current = None
	frontier = PriorityQueue()
	cost_so_far = {start: 0}
	came_from = defaultdict(set)  # This set stores ALL shortest paths (for part B)
	frontier.put((cost_so_far[start], start))

	while frontier:
		current = frontier.get()[1]

		if current == end:
			break

		for neighbour in graph_.neighbours(current):
			new_cost = cost_so_far[current] + graph_.cost(current, neighbour)

			# Usual Dijkstra code to establish a shortest path
			if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
				cost_so_far[neighbour] = new_cost
				came_from[neighbour].add(current)
				frontier.put((new_cost, neighbour))

			# To store ALL shortest paths (for part B)
			elif new_cost == cost_so_far[neighbour]:
				came_from[neighbour].add(current)

	return cost_so_far.get(current), came_from


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

# Part A
# Note there is only one way to reach end goal in my real input (has to move in E direction)
graph = Graph(parse_input(REAL_INPUT))
starting_pos, ending_pos = get_start_end_locations(graph)
lowest_cost, all_shortest_paths = dijkstra_shortest_path(starting_pos, ending_pos, graph)
print(f'Part A: {lowest_cost}')

# Part B
# BFS along the path from end to start (i.e. traverse all shortest paths)
# Along the way, record all visited nodes (along any shortest path) in a set
current = ending_pos
all_visited = set()
path = deque()  # Using this like a simple queue
path.append(current)
while path:
	current = path.popleft()
	all_visited.add((current.row, current.col))
	for tile in all_shortest_paths[current]:
		if tile not in path:
			path.append(tile)
print(f'Part B: {len(all_visited)}')
