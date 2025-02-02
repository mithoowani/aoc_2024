from collections import defaultdict

TEST_INPUT = """029A
980A
179A
456A
379A"""


def shortest_dpad_path(start_key, end_key):
	"""Returns shortest path from one dpad button to another
	Directional pad:
		+---+---+
		| ^ | A |
	+---+---+---+
	| < | v | > |
	+---+---+---+

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

	From reddit, every single path from one dpad direction to another
	paths = {
		'A': {"A": [""], "^": ["<"], ">": ["v"], "v": ["<v", "v<"], "<": ["<v<", "v<<"]},
		'^': {"^": [""], "A": [">"], "v": ["v"], "<": ["v<"], ">": ["v>"]},
		'v': {"v": [""], "A": ["^>", ">^"], "^": ["^"], "<": ["<"], ">": [">"]},
		'<': {"<": [""], "A": [">>^", ">^>"], "^": [">^"], "v": [">"], ">": [">>"]},
		'>': {">": [""], "A": ["^"], "^": ["^<", "<^"], "v": ["<"], "<": ["<<"]},
	}

	My guess at the optimal paths between keypad buttons
	General principles are that:
	Repeated moves are preferable (e.g. >>~^ over >^>)
	Cost from worst to best based on relative locations on the keypad and confirmed by my testing
	<A ; vA ; ^A ; >A   [not 100% sure about ^A versus >A]
	e.g.; <A produces a long sequence when traveling from < back to A

	"""

	paths = {
		'A': {"A": [""], "^": ["<"], ">": ["v"], "v": ["<v"], "<": ["v<<"]},
		'^': {"^": [""], "A": [">"], "v": ["v"], "<": ["v<"], ">": ["v>"]},
		'v': {"v": [""], "A": ["^>"], "^": ["^"], "<": ["<"], ">": [">"]},
		'<': {"<": [""], "A": [">>^"], "^": [">^"], "v": [">"], ">": [">>"]},
		'>': {">": [""], "A": ["^"], "^": ["<^"], "v": ["<"], "<": ["<<"]},
	}

	return paths[start_key][end_key][0] + 'A'


def get_sequence(key_combination: str):
	"""For a given directional key combination on a dpad, returns the
	 key combination of the next robot in line, e.g. >A --> vA^A if starting from A"""

	sequence = []
	start = 'A'
	for char in key_combination:
		end = char
		sequence.extend(shortest_dpad_path(start, end))
		start = char

	return ''.join(sequence)


def memoized_calculate_length(sequence, depth, max_depth):
	"""Takes a given sequence and reurns the optimal length of the human button presses if max_depth robots
	separate the human from the keypad"""

	memo = defaultdict(lambda: 0)

	def calculate_length(sequence, depth, max_depth):
		nonlocal memo
		if depth >= max_depth:
			return len(sequence)
		elif not memo.get((depth, sequence)):
			for substring in [subsequence + 'A' for subsequence in sequence.split('A')[:-1]]:
				next_sequence = get_sequence(substring)
				memo[(depth, sequence)] += calculate_length(next_sequence, depth + 1, max_depth)

		return memo[(depth, sequence)]

	return calculate_length(sequence, depth, max_depth)


# This is what came out in a breadth first search (shortest path) of keypresses for the first robot's
# directional pad, but it has some suboptimal mvoves as per the rules I created above;
# e.g. ^^<A is worse than <^^A in 938A
real_inputs_auto = {'480A': '^^<<A^>AvvvA>A',
					'682A': '^^A^<AvvAv>A',
					'140A': '^<<A^Av>vA>A',
					'246A': '^<A^<A>>AvvA',
					'938A': '^^^AvvA^^<Avvv>A'}

# I manually modified this manually based on the rules above; and it generated a correct answer to part A
real_inputs_optimal = {'480A': '^^<<A^>AvvvA>A',
					   '682A': '^^A<^AvvAv>A',
					   '140A': '^<<A^A>vvA>A',
					   '246A': '<^A<^A>>AvvA',
					   '938A': '^^^AvvA<^^Avvv>A'}

# Part A is a depth of 3 (keypad input; then 2 inputs on top of that)
part_A = 0
for line, keypad_input in real_inputs_optimal.items():
	part_A += memoized_calculate_length(keypad_input, depth=1, max_depth=3) * int(line[:-1])
print(f'{part_A=}')

# Part B is a depth of 26
part_B = 0
for line, keypad_input in real_inputs_optimal.items():
	part_B += memoized_calculate_length(keypad_input, depth=1, max_depth=26) * int(line[:-1])
print(f'{part_B=}')
