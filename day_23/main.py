from collections import defaultdict, deque
from pprint import pprint

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
