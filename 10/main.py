from pprint import pprint
import numpy as np

TEST_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


class Vertex:
	"""
	A simple class representing a vertex in a graph
	"""

	def __init__(self, value):
		self.value = value
		self.adjacent_vertices = []

	def add_adjacent_vertex(self, *vertices):
		for vertex in vertices:
			if vertex not in self.adjacent_vertices:
				self.adjacent_vertices.append(vertex)
				vertex.add_adjacent_vertex(self)  # bidirectional relationship

	def __repr__(self):
		return f'{self.value}'


def parse_input(puzzle_input):
	"""
	Returns 1) puzzle input as a 2-d numpy array and 2) a list of all vertices
	"""
	vertices = {}
	array = puzzle_input.split('\n')
	array_lists = []
	for i, line in enumerate(array):
		array_lists.append(list(line))

		# Add one to row and column because the array ends up padded with a border of -1's at the end
		for j, element in enumerate(line):
			vertices[(i + 1, j + 1)] = Vertex(int(element))

	return np.array(array_lists).astype('int64'), vertices


def create_graph(padded_array, _vertices) -> list[Vertex]:
	"""
	Creates a graph representing relationship between all vertices
	and returns a list of starting points (all vertices with a value of 0)
	"""
	starting_vertices = []

	for i, row in enumerate(padded_array):
		for j, val in enumerate(row):

			# ignore padding
			if val == -1:
				continue

			current_vertex = Vertex(val)

			neighbours = {
				'up': _vertices.get((i - 1, j)),
				'down': _vertices.get((i + 1, j)),
				'left': _vertices.get((i, j - 1)),
				'right': _vertices.get((i, j + 1))
			}

			current_vertex.add_adjacent_vertex(*[neighbour for neighbour in neighbours.values()
												 if (neighbour is not None and neighbour.value > -1)])

			if val == 0:
				starting_vertices.append(current_vertex)

	return starting_vertices

def traverse_graph_a(vertex, visited=None):
	if visited is None:
		visited = {}

	visited[vertex] = True

	if vertex.value == 9:
		unique_endings.add(vertex)

	for adjacent in vertex.adjacent_vertices:
		if visited.get(adjacent) is True:
			continue
		else:
			if adjacent.value - vertex.value == 1:
				traverse_graph_a(adjacent, visited)

def traverse_graph_b(vertex):
	"""For Part B, counts all paths to a 9;
	in other words, visiting the same square twice is allowed"""
	global count

	for adjacent in vertex.adjacent_vertices:
		if adjacent.value - vertex.value == 1:
			if adjacent.value == 9:
				count += 1
			else:
				traverse_graph_b(adjacent)


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

array, vertices = parse_input(REAL_INPUT)

# pad array with a border of -1's to avoid out-of-bounds error when checking neighbours
# noinspection PyTypeChecker
array = np.pad(array, ((1, 1), (1, 1)), constant_values=-1)

starting_points = create_graph(array, vertices)

# Part A
scores = 0
for start in starting_points:
	unique_endings = set()  # set to avoid duplicate paths to a single 9
	traverse_graph_a(start)
	scores += len(unique_endings)
print(f'Part A: {scores}')

# Part B
count = 0
for start in starting_points:
	traverse_graph_b(start)
print(f'Part B: {count}')
