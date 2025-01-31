from dataclasses import dataclass
from pprint import pprint
from collections import deque
import random
import numpy as np

TEST_INPUT = """029A
980A
179A
456A
379A"""


class Pad:
	def __init__(self):
		self.key_to_coord = {}
		self.coord_to_key = {}

	def get_neighbours(self, key: str):
		neighbours = {}
		row, col = self.key_to_coord[key]

		# TODO: I think it it needs to prioritize the shortest path with the least number of "turns"
		# In other words v<< (1 turn) is better than <v< (2 turns); if this assumption is wrong then you would have to DFS
		# all possible paths!! To make sure this is the right assumption, could try to manually correct some
		# paths to see if you get the right solution

		# Maybe Dijkstra shortest path; cost=1 if same direction, cost=2 otherwise?

		# Maybe you calculate all BFS solutions; then iterate through string and choose the one with the longest
		# unidirectional sequence; e.g. 7 to 0; >vvv would be preferred over vv>v (anytime a character changes
		# a penalty of 1 is added to the score)

		# Or sort the shortest path before returning it? ** This will produce some invalid paths
		for direction, coord in {'v': (row + 1, col),
								 '^': (row - 1, col),
								 '<': (row, col - 1),
								 '>': (row, col + 1)}.items():

			if coord in self.coord_to_key:
				neighbours[direction] = self.coord_to_key[coord]

		# TODO: Randomizing the order of neighbours is an extremely hacky way of solving part 1
		list_neighbours = list(neighbours.items())
		random.shuffle(list_neighbours)
		neighbours = dict(list_neighbours)

		return neighbours

	def shortest_path(self, start_key: str, end_key: str):

		# TODO: This hard coding seems to work for the Dpad but not generalizable to the numpad
		# TODO: Write a Dijkstra algorithm that penalizes turns probably
		if start_key == '<' and end_key == 'A':
			return list('>>^A')

		elif start_key == 'A' and end_key == '<':
			return list('v<<A')

		came_from = {start_key: None}
		frontier = deque([start_key])

		while frontier:
			current_key = frontier.popleft()
			if current_key == end_key:
				break
			for direction, neighbour in self.get_neighbours(current_key).items():
				if neighbour not in came_from:
					came_from[neighbour] = (direction, current_key)
					frontier.append(neighbour)

		directions = []
		current_key = came_from[end_key]

		while current_key:
			directions.append(current_key[0])
			current_key = came_from[current_key[1]]
		directions.reverse()
		directions.append('A')
		return directions


class Keypad(Pad):
	def __init__(self):
		super().__init__()
		"""
		Keypad:
		+---+---+---+
		| 7 | 8 | 9 |
		+---+---+---+
		| 4 | 5 | 6 |
		+---+---+---+
		| 1 | 2 | 3 |
		+---+---+---+
			| 0 | A |
    		+---+---+
		"""
		self.key_to_coord = {'7': (0, 0),
							 '8': (0, 1),
							 '9': (0, 2),
							 '4': (1, 0),
							 '5': (1, 1),
							 '6': (1, 2),
							 '1': (2, 0),
							 '2': (2, 1),
							 '3': (2, 2),
							 '0': (3, 1),
							 'A': (3, 2)}

		self.coord_to_key = {value: key for key, value in self.key_to_coord.items()}


class DPad(Pad):
	def __init__(self):
		super().__init__()
		"""
		Directional pad:
				+---+---+
				| ^ | A |
			+---+---+---+
			| < | v | > |
			+---+---+---+
		"""
		self.key_to_coord = {'^': (0, 1),
							 'A': (0, 2),
							 '<': (1, 0),
							 'v': (1, 1),
							 '>': (1, 2)}

		self.coord_to_key = {value: key for key, value in self.key_to_coord.items()}


def get_sequence(key_combination: str, pad: Pad):
	sequence = []
	start = 'A'
	for char in key_combination:
		end = char
		sequence.extend(pad.shortest_path(start, end))
		start = char

	return ''.join(sequence)


min_A = None

keypad = Keypad()
dpad = DPad()

with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

for _ in range(10_000):
	part_A = 0

	for key_combination in REAL_INPUT.split('\n'):
		level_1 = get_sequence(key_combination, keypad)
		level_2 = get_sequence(level_1, dpad)
		level_3 = get_sequence(level_2, dpad)
		# print(level_1, '\n', level_2, '\n', level_3)
		# print(len(level_3), int(key_combination[:-1]))
		# print()

		part_A += len(level_3) * int(key_combination[:-1])

	if min_A is None or part_A < min_A:
		min_A = part_A

print(min_A)
print()


level_1 = '^A<<^^A>>AvvvA'  # <<^^A is preferred to ^^<<A
level_2 = get_sequence(level_1, dpad)
level_3 = get_sequence(level_2, dpad)
print(level_1, '\n', level_2, '\n', level_3)
print(len(level_3), 379)
print()


# WRONG: <AAA>Av<<A>^>Av<AAA^>AvA^A   -> the >^> adds an unnecessary turn compared to >>^ or ^>> [latter is invalid] to get from < to A
# WRONG: v<<A>^>AAAvA^Av<A<AA>^>AvA^<Av>A^Av<A<A>^>AAA<Av>A^Av<A^>A<A>A (62 980)
# RIGHT: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A (60 980)

# third_sequence = []
# start = 'A'
# for char in '<AAA>Av<<A>>^Av<AAA^>AvA^A':  # corrected string with minimal turns (>>^)
# 	end = char
# 	third_sequence.extend(dpad.shortest_path(start, end))
# 	start = char
# print()
# print(''.join(third_sequence))
# print(len(third_sequence))

# For part 2 potentially
# instructions = [sequence + 'A' for sequence in ''.join(second_sequence).split('A')[:-1]]
