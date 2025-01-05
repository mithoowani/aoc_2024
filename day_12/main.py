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


def parse_input(puzzle_input):
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


def populate(vert, array, seen=None):
	"""
	Returns the area and perimeter of an island starting at vert
	"""

	if seen is None:
		seen = {}

	i, j = vert.location[0], vert.location[1]
	seen[(i, j)] = vert

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


def get_perimeter(_island):
	perimeter = 0
	for vertex in _island.values():
		perimeter += 4 - len(vertex.adjacent_vertices)
	return perimeter


def get_sides(_island, side='left'):
	num_sides = 0
	squares_with_free_side = [location for location, vertex in _island.items() if vertex.free_sides[side] is True]
	if side in ['left', 'right']:
		squares_with_free_side.sort(key=lambda x: (x[1], x[0]))
	else:
		squares_with_free_side.sort(key=lambda x: (x[0], x[1]))

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


def get_total_sides(_island):
	total_slides = sum([get_sides(_island, side) for side in 'left right top bottom'.split()])
	return total_slides


# right_side_free = [location for location, vertex in _island if vertex.free_sides['right'] is True]
#
#
# top_side_free = [location for location, vertex in _island if vertex.free_sides['top'] is True]
#
#
# bottom_side_free = [location for location, vertex in _island if vertex.free_sides['bottom'] is True]


def populate_islands(array: np.array):
	all_visited = {}
	answers = []
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
			answers.append((str(start.value), area * perimeter))
			answers_b.append((str(start.value), area * sides))
	# print(f'{start.value}: {area} * {perimeter} = {area * perimeter}')
	return answers_b


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

puzzle_array = parse_input(REAL_INPUT)
scores = populate_islands(puzzle_array)

# Part A

# pprint(scores)
# total_score = sum(score[1] for score in scores)
# print(total_score)

# Part B
pprint(scores)
total_score = sum(score[1] for score in scores)
print(total_score)
