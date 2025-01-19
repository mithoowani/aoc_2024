"""
Graph/location data structure and algorithms inspired by:
https://www.redblobgames.com/pathfinding/a-star/introduction.html
"""

from collections import defaultdict, deque
from queue import PriorityQueue
from pprint import pprint
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


@dataclass(frozen=True, order=True)
class Location:
	row: int
	col: int
	dir: str  # direction N, S, E, W


class Graph:
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
	start_loc = int(np.where(graph_.graph == 'S')[0][0]), int(np.where(graph.graph == 'S')[1][0])
	end_loc = int(np.where(graph_.graph == 'E')[0][0]), int(np.where(graph.graph == 'E')[1][0])

	# hard coded --
	start = Location(start_loc[0], start_loc[1], 'E')
	# two possible representations of the end tile
	end_1 = Location(end_loc[0], end_loc[1], dir='E')
	end_2 = Location(end_loc[0], end_loc[1], dir='N')

	return start, end_1, end_2


def dijkstra_shortest_path(start, end, graph_):
	# Frontier is a priority queue, so that it remains sorted by priority (cost)
	# Entries are in the form (cost, location)
	current = None
	frontier = PriorityQueue()
	cost_so_far = {start: 0}
	came_from = defaultdict(set)
	frontier.put((cost_so_far[start], start))

	while frontier:
		current = frontier.get()[1]

		if current == end:
			break

		for neighbour in graph_.neighbours(current):
			new_cost = cost_so_far[current] + graph_.cost(current, neighbour)
			if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
				cost_so_far[neighbour] = new_cost
				came_from[neighbour].add(current)
				frontier.put((new_cost, neighbour))
			elif new_cost == cost_so_far[neighbour]:
				came_from[neighbour].add(current)

	return cost_so_far.get(current), came_from


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

# for test input; two possible ways to reach end goal
# graph = Graph(parse_input(TEST_INPUT_2))
# start, end_1, end_2 = get_start_end_locations(graph)
# shortest_path_1, path_1 = dijkstra_shortest_path(start, end_1, graph)
# shortest_path_2, path_2 = dijkstra_shortest_path(start, end_2, graph)

# for real input, only one way to reach end goal
graph = Graph(parse_input(REAL_INPUT))
start, end_east, end_north = get_start_end_locations(graph)
shortest_path, path_2 = dijkstra_shortest_path(start, end_east, graph)
print(f'Part A: {shortest_path}')

# do a depth first search along the path going from end to start (traverse all shortest paths)
# record all visited nodes along ANY shortest path
current = end_east
all_visited = set()
path = deque()
path.append(current)
while path:
	current = path.popleft()
	all_visited.add((current.row, current.col))
	for tile in path_2[current]:
		if tile not in path:
			path.append(tile)
print(f'Part B: {len(all_visited)}')
