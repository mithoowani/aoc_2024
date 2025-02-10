from collections import defaultdict, deque
from pprint import pprint
from copy import copy

TEST_INPUT = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

pcs = defaultdict(list)
for line in REAL_INPUT.split('\n'):
	pc_1, pc_2 = line.split('-')
	pcs[pc_1].append(pc_2)
	pcs[pc_2].append(pc_1)


def search_cycle(start: str):
	# cycles is a set so that duplicates aren't recorded
	cycles = set()

	frontier = deque([start])
	came_from = {start: None}

	while frontier:
		current = frontier.popleft()

		for neighbour in pcs[current]:
			if neighbour not in came_from:
				came_from[neighbour] = current
				frontier.append(neighbour)

			# neighbour has already been visited but is not the parent of the current node
			elif neighbour != came_from[current]:

				# this forms a triangle for part A
				if came_from[neighbour] == start and came_from[current] == start:
					cycles.add(tuple(sorted([start, neighbour, current])))

	return cycles


def is_clique(potential_clique: set[str]):
	"""Checks whether each node in the potential_clique is connected to every other node; if True then
	it satisfies the definition of a clique"""
	potential_clique = list(potential_clique)
	for i, pc_1 in enumerate(potential_clique):
		for j in potential_clique[i + 1:]:
			if j not in pcs[pc_1]:
				return False
	return True


def find_largest_clique(current, clique=None):
	"""Simple DFS to traverse the graph, adding one node at a time only if it meets the definition of a clique"""
	if clique is None:
		clique = set()

	for neighbour in pcs[current]:
		if neighbour not in clique:
			longer_clique = copy(clique)
			longer_clique.add(neighbour)
			if is_clique(longer_clique):
				clique = find_largest_clique(neighbour, longer_clique)

	return clique


# the same cycle can be recorded from a different start position, e.g. (co, ka, ta) and (ka, co, ta)
# so delete duplicates again
all_unique_cycles = set()
for start in pcs:
	all_cycles = tuple(sorted(search_cycle(start)))
	for cycle in all_cycles:
		all_unique_cycles.add(cycle)

# now count up all cycles with at least one computer starting in 't'
part_A = 0
for cycle in all_unique_cycles:
	for pc in cycle:
		if pc.startswith('t'):
			part_A += 1
			break
print(f'{part_A=}')

# Brute force approach to Part B
all_cliques = set()
for start in pcs:
	all_cliques.add(tuple(sorted(find_largest_clique(start))))
part_B = ','.join(sorted(all_cliques, key=lambda x: len(x), reverse=True)[0])
print(f'{part_B=}')
