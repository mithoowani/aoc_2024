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

		return neighbours


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

	def shortest_path(self, start_key, end_key):
		# from reddit, original
		# paths = {
		# 	'A': {"A": [""], "^": ["<"], ">": ["v"], "v": ["<v", "v<"], "<": ["<v<", "v<<"]},
		# 	'^': {"^": [""], "A": [">"], "v": ["v"], "<": ["v<"], ">": ["v>"]},
		# 	'v': {"v": [""], "A": ["^>", ">^"], "^": ["^"], "<": ["<"], ">": [">"]},
		# 	'<': {"<": [""], "A": [">>^", ">^>"], "^": [">^"], "v": [">"], ">": [">>"]},
		# 	'>': {">": [""], "A": ["^"], "^": ["^<", "<^"], "v": ["<"], "<": ["<<"]},
		# }

		# My guess at the optimal paths between keypad buttons
		# General principles are that:
		# Repeated moves are preferable (e.g. >>^ over >^>)
		# Cost from worst to best based on relative locations in keypad and testing
		# <A ; vA ; ^A ; >A   [not 100% sure about ^A versus >A]

		paths = {
			'A': {"A": [""], "^": ["<"], ">": ["v"], "v": ["<v"], "<": ["v<<"]},
			'^': {"^": [""], "A": [">"], "v": ["v"], "<": ["v<"], ">": ["v>"]},
			'v': {"v": [""], "A": ["^>"], "^": ["^"], "<": ["<"], ">": [">"]},
			'<': {"<": [""], "A": [">>^"], "^": [">^"], "v": [">"], ">": [">>"]},
			'>': {">": [""], "A": ["^"], "^": ["<^"], "v": ["<"], "<": ["<<"]},
		}

		return paths[start_key][end_key][0] + 'A'


def get_sequence(key_combination: str, pad: Pad):
	sequence = []
	start = 'A'
	for char in key_combination:
		end = char
		sequence.extend(pad.shortest_path(start, end))
		start = char

	return ''.join(sequence)


keypad = Keypad()
dpad = DPad()

# This is what came out in a breadth first search (shortest path)
real_inputs_auto = {'480A': '^^<<A^>AvvvA>A',
					'682A': '^^A^<AvvAv>A',
					'140A': '^<<A^Av>vA>A',
					'246A': '^<A^<A>>AvvA',
					'938A': '^^^AvvA^^<Avvv>A'}

# I modified this manually based on the rules above; and it generated a correct answer to part A
real_inputs_optimal = {'480A': '^^<<A^>AvvvA>A',
					   '682A': '^^A<^AvvAv>A',
					   '140A': '^<<A^A>vvA>A',
					   '246A': '<^A<^A>>AvvA',
					   '938A': '^^^AvvA<^^Avvv>A'}

# Part A is the keypad input, and then two robots on top of that
part_A = 0
for line, keypad_input in real_inputs_optimal.items():
	sequence_1 = get_sequence(keypad_input, dpad)
	sequence_2 = get_sequence(sequence_1, dpad)
	part_A += len(sequence_2) * int(line[:-1])
print(f'{part_A=}')

# Part B is the keypad input followed by 25 additional sequences on top
# TOO INEFFICIENT
part_B = 0
for line, keypad_input in real_inputs_optimal.items():
	sequence = get_sequence(keypad_input, dpad)
	for i in range(24):
		sequence = get_sequence(sequence, dpad)
	part_B += len(sequence) * int(line[:-1])
print(f'{part_B=}')
