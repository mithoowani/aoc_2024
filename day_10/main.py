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
	# Return puzzle input as a 2-d numpy array and a list of all vertices
	vertices = {}
	array = puzzle_input.split('\n')
	array_lists = []
	for i, line in enumerate(array):
		array_lists.append(list(line))

		for j, element in enumerate(line):
			vertices[(i + 1, j + 1)] = Vertex(int(element))

	return np.array(array_lists).astype('int64'), vertices


def create_graph(padded_array, _vertices) -> list[Vertex]:
	"""Creates a graph and returns a list of starting points (Vertices with a value of 0)"""
	starting_vertices = []

	for i, row in enumerate(padded_array):
		for j, val in enumerate(row):

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


def traverse_graph(vertex, visited=None):
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
				traverse_graph(adjacent, visited)


with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

array, vertices = parse_input(REAL_INPUT)
# noinspection PyTypeChecker
array = np.pad(array, ((1, 1), (1, 1)), constant_values=-1)
starting_points = create_graph(array, vertices)

scores = 0
for start in starting_points:
	unique_endings = set()
	traverse_graph(start)
	scores += len(unique_endings)

print(f'Part A: {scores}')
