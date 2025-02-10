from dataclasses import dataclass
from collections import deque
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
		"""Returns neighbours of the current location"""

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

	def print_path(self, path):
		"""Helper function that displays the shortest path"""
		for location in path:
			self.graph[location.row, location.col] = 'O'
		print(str(self))

	def __str__(self):
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


def bfs_shortest_path(start, end, graph_):
	"""Simple BFS for a 2D graph"""
	frontier = deque([start])
	came_from = {start: None}

	while frontier:
		current = frontier.popleft()

		if current == end:
			break

		for neighbour in graph_.neighbours(current):
			if neighbour not in came_from:
				came_from[neighbour] = current
				frontier.append(neighbour)

	return came_from


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

# In retrospect, because there is only one path from start to end, the graph/BFS search is way overkill... oh well
graph = Graph(parse_input(REAL_INPUT))
start, end = get_start_end_locations(graph)
path = bfs_shortest_path(start, end, graph)
shortest_path = generate_shortest_path(path, start, end)

# a dictionary that maps every location to distance from the endpoint
distances = {location: distance for distance, location in enumerate(reversed(shortest_path))}

minimum_time_to_save = 100  # for real input in Part A/B
cheat_duration_a = 2  # 2 picoseconds for part A
cheat_duration_b = 20  # 20 picoseconds for part B

# Approach is to iterate through the shortest path and identify all possible cheats;
# i.e. squares further along the path that can be reached within 2 picoseconds (for part A) or
# 20 picoseconds (for part B) by calculating Manhattan distance from the current locaton
# If the time_saved is >= 100 picoseconds, then count it

part_A = 0
part_B = 0
for i, start in enumerate(shortest_path):
	for j, end in enumerate(shortest_path[i:]):
		manhattan_distance = abs(start.row - end.row) + abs(start.col - end.col)

		# time saved is: time needed to reach goal from original square along shortest path
		# 				 - time needed to reach goal from new "cheat" square
		# 				 - time spent traveling from the original to the cheat square
		time_saved = distances[start] - distances[end] - manhattan_distance

		if time_saved >= minimum_time_to_save:
			if manhattan_distance <= cheat_duration_a:
				part_A += 1
			if manhattan_distance <= cheat_duration_b:
				part_B += 1

print(f'Part A: {part_A}')
print(f'Part B: {part_B}')
