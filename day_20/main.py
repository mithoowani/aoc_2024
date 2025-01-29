from queue import PriorityQueue
from dataclasses import dataclass
from collections import Counter, defaultdict
from pprint import pprint
from time import time
import numpy as np

TEST_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


# Frozen allows hashing of the resulting objects; order allows them to be used in a priority queue
@dataclass(frozen=True, order=True)
class Location:
	row: int
	col: int


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

		# no neighbours because location is invalid
		if not self.in_bounds(loc) or not self.passable(loc):
			return []

		directions = {'up': Location(loc.row - 1, loc.col),
					  'down': Location(loc.row + 1, loc.col),
					  'right': Location(loc.row, loc.col + 1),
					  'left': Location(loc.row, loc.col - 1)}

		neighbours = [direction for direction in directions.values() if
					  self.in_bounds(direction) and self.passable(direction)]

		return neighbours

	@staticmethod
	def cost(loc1: Location, loc2: Location):
		"""Returns cost associated with moving from loc1 to loc2"""
		if abs(loc1.row - loc2.row) + abs(loc1.col - loc2.col) == 1:
			return 1
		else:
			raise Exception('Not neighbours')

	def print_path(self, path):
		"""Helper function that displays the shortest path"""
		for location in path:
			self.graph[location.row, location.col] = 'O'
		print(str(self))

	def __str__(self):
		for line in self.graph:
			string_line = '\n'.join([''.join(list(line)) for line in self.graph])
		return string_line


def parse_input(puzzle_input: str):
	"""Converts puzzle input (string) into np array"""
	maze_lists = []
	for line in puzzle_input.split('\n'):
		maze_lists.append(list(line))
	maze_array = np.array(maze_lists)
	return maze_array


def get_start_end_locations(graph_: Graph):
	"""Returns location of the start and end positions as Location objects"""
	start_loc = int(np.where(graph_.graph == 'S')[0][0]), int(np.where(graph_.graph == 'S')[1][0])
	end_loc = int(np.where(graph_.graph == 'E')[0][0]), int(np.where(graph_.graph == 'E')[1][0])

	start = Location(start_loc[0], start_loc[1])
	end = Location(end_loc[0], end_loc[1])

	return start, end


def heuristic(loc1: Location, loc2: Location):
	"""Returns Manhattan distance between loc1 and loc2"""
	return abs(loc1.row - loc2.row) + abs(loc1.col - loc2.col)


def a_star_shortest_path(start, end, graph_):
	# Frontier is a priority queue, so that it remains sorted by priority (cost)
	# Entries in the priority queue are in the form (cost, location)
	current = None
	frontier = PriorityQueue()
	cost_so_far = {start: 0}
	came_from = dict()
	frontier.put((cost_so_far[start], start))

	while frontier:
		current = frontier.get()[1]

		if current == end:
			break

		for neighbour in graph_.neighbours(current):
			new_cost = cost_so_far[current] + graph_.cost(current, neighbour)

			if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
				cost_so_far[neighbour] = new_cost
				came_from[neighbour] = current
				frontier.put((new_cost + heuristic(neighbour, end), neighbour))

	return cost_so_far.get(current), came_from


def generate_shortest_path(path_, start_, end_):
	"""Helper function that returns the shortest path from start to end in a list"""
	start_to_finish = []
	current = end_
	while current != start_:
		start_to_finish.append(current)
		current = path_[current]
	start_to_finish.append(current)
	start_to_finish.reverse()
	return start_to_finish


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

# start_time = time()
graph = Graph(parse_input(REAL_INPUT))
start, end = get_start_end_locations(graph)
total_cost, path = a_star_shortest_path(start, end, graph)
# print(f'{start=}, {end=}')
# print(f'{total_cost=}')
shortest_path = generate_shortest_path(path, start, end)
distances = {location: distance for distance, location in enumerate(reversed(shortest_path))}
# pprint(distances)
shortcuts = defaultdict(list)

minimum_time_to_save = 100  # for real input in Part A/B

# PART A
for loc in shortest_path:
	r, c = loc.row, loc.col
	moves = (Location(r - 2, c), Location(r + 2, c), Location(r, c - 2), Location(r, c + 2),
			 Location(r - 1, c - 1), Location(r - 1, c + 1), Location(r + 1, c - 1), Location(r + 1, c + 1))

	for move in moves:
		if graph.passable(move) and graph.in_bounds(move):
			time_saved = distances[loc] - distances[move] - 2
			shortcuts[loc].append(time_saved if time_saved > 0 else 0)
# pprint(shortcuts)
num_shortcuts = Counter()
for time_saved in shortcuts.values():
	num_shortcuts.update(time_saved)
num_shortcuts = dict(num_shortcuts)
# pprint(num_shortcuts)

answer = 0
for time_saved, num in num_shortcuts.items():
	if time_saved >= minimum_time_to_save:
		answer += num
print(f'Part A: {answer}')

# PART B try 2
count = 0
for i, start in enumerate(shortest_path):
	for j, end in enumerate(shortest_path[i:]):
		manhattan_distance = abs(start.row - end.row) + abs(start.col - end.col)
		if manhattan_distance <= 20:
			time_saved = distances[start] - distances[end] - manhattan_distance
			if time_saved >= minimum_time_to_save:
				count += 1
print(f'Part B: {count}')

# TODO: Get rid of the A* algorithm because there's only one path (one neighbour per tile)
# TODO: Optimize part A to make it more consistent with part B
