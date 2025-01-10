from pprint import pprint
import numpy as np

TEST_INPUT_1 = """AAAA
BBCD
BBCC
EEEC"""

TEST_INPUT_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

TEST_INPUT_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

TEST_INPUT_4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

TEST_INPUT_5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


class Vertex:
	"""
	A simple class representing a vertex in a graph
	"""

	def __init__(self, value, location):
		self.value = value
		self.location = location
		self.adjacent_vertices = []

		# Used in part b
		# Represents sides that have "free" edges
		self._free_sides = {
			'left': True,
			'right': True,
			'top': True,
			'bottom': True
		}

	def add_adjacent_vertex(self, *vertices):
		for vertex in vertices:
			if vertex not in self.adjacent_vertices:
				self.adjacent_vertices.append(vertex)
				vertex.add_adjacent_vertex(self)  # bidirectional relationship

	@property
	def free_sides(self):
		"""
		Returns the vertex's free sides by examining its neighbours
		"""
		i, j = self.location[0], self.location[1]

		for neighbour in self.adjacent_vertices:
			if neighbour.location == (i + 1, j):
				self._free_sides['bottom'] = False
			elif neighbour.location == (i - 1, j):
				self._free_sides['top'] = False
			elif neighbour.location == (i, j + 1):
				self._free_sides['right'] = False
			elif neighbour.location == (i, j - 1):
				self._free_sides['left'] = False

		return self._free_sides

	def __repr__(self):
		return f'{self.value}'


def parse_input(puzzle_input: str):
	"""
	Return puzzle input as a 2-d numpy array, padded with '0' values
	"""

	array = puzzle_input.split('\n')
	array_lists = []
	for line in array:
		array_lists.append(list(line))
	unpadded_array = np.array(array_lists)
	padded_array = np.pad(unpadded_array, ((1, 1), (1, 1)), constant_values='0')

	return padded_array


def populate(vert: Vertex, array: np.array, seen=None) -> dict:
	"""
	Returns a list of all tiles in an island starting at the vertex "vert"
	"""

	# dictionary with key = coordinate, value = Vertex with that coordinate
	if seen is None:
		seen = {}

	i, j = vert.location[0], vert.location[1]
	seen[(i, j)] = vert

	# coordinates for all of vert's neighbours
	neighbours = {
		'up': (i - 1, j),
		'down': (i + 1, j),
		'left': (i, j - 1),
		'right': (i, j + 1)
	}

	for neighbour in neighbours.values():
		if array[neighbour[0], neighbour[1]] == vert.value and not seen.get(neighbour):
			new_vertex = Vertex(value=vert.value, location=neighbour)
			vert.add_adjacent_vertex(new_vertex)
			populate(new_vertex, array, seen)
		elif seen.get(neighbour):
			vert.add_adjacent_vertex(seen.get(neighbour))

	return seen


def get_perimeter(_island: dict) -> int:
	"""Returns perimeter of the island (for part a)"""
	perimeter = 0
	for vertex in _island.values():
		perimeter += 4 - len(vertex.adjacent_vertices)
	return perimeter


def get_sides(_island: dict, side='left') -> int:
	"""
	Returns the number of left, right, top and bottom sides of the island (for part b)
	"""

	num_sides = 0
	squares_with_free_side = [location for location, vertex in _island.items() if vertex.free_sides[side] is True]
	if side in ['left', 'right']:
		squares_with_free_side.sort(key=lambda x: (x[1], x[0]))  # sort by col first, then row
	else:
		squares_with_free_side.sort(key=lambda x: (x[0], x[1]))  # sort by row first, then col

	# The approach is to iterate through every square with the free side
	# If the next square in the sorted list is a neighbour (e.g. same row but col differs by only 1) then it's part of the
	# same side, otherwise it's part of a new side (and num_sides is incremented by 1)
	current_square = None
	for square in squares_with_free_side:
		if current_square is None:
			num_sides += 1
		elif side in ['top', 'bottom'] and abs(square[1] - current_square[1]) == 1 and square[0] == current_square[0]:
			pass
		elif side in ['left', 'right'] and abs(square[0] - current_square[0]) == 1 and square[1] == current_square[1]:
			pass
		else:
			num_sides += 1
		current_square = square

	return num_sides


def get_total_sides(_island: dict) -> int:
	"""Returns the total sides of the island (for part b)"""
	total_slides = sum([get_sides(_island, side) for side in 'left right top bottom'.split()])
	return total_slides


def solve_puzzle(array: np.array):
	"""
	Solves parts a and b
	Approach is to iterates through every square; when a previously unvisited square is encountered,
	populates the island and calculates its relevant parameters (area, perimeters, num_sides)
	"""
	all_visited = {}
	answers_a = []
	answers_b = []

	for i in range(array.shape[0]):
		for j in range(array.shape[1]):
			if array[i, j] == '0':  # ignore padded values
				continue

			elif all_visited.get((i, j)):
				continue

			else:
				start = Vertex(value=array[i, j], location=(i, j))
				island = populate(start, array)
				for entry in island:
					all_visited[entry] = True

			area = len(island)
			perimeter = get_perimeter(island)
			sides = get_total_sides(island)
			answers_a.append((str(start.value), area * perimeter))
			answers_b.append((str(start.value), area * sides))

	return answers_a, answers_b


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

puzzle_array = parse_input(REAL_INPUT)
scores_a, scores_b = solve_puzzle(puzzle_array)

# Part A
# pprint(scores_a)
total_score = sum(score[1] for score in scores_a)
print(f'Part A: {total_score}')

# Part B
# pprint(scores_b)
total_score = sum(score[1] for score in scores_b)
print(f'Part B: {total_score}')
