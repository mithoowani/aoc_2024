from functools import cache

TEST_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


def parse_input(puzzle):
	letters = {}
	for letter in puzzle.split('\n\n')[0].split(', '):
		letters[letter] = True
	words = [line for line in puzzle.split('\n\n')[1].split('\n')]
	return letters, words


# REMEMBER TO ADJUST MAX_LEN DEPENDING ON TEST OR REAL INPUT
@cache
def is_possible(arrangement, pointer=0, max_len=8, sequences=0):
	"""
	Returns number of ways the arrangement can be made with the available towels (answer to part B).

	max_len is the longest pattern in a single towel from the puzzle input (this would be 3 in the TEST_INPUT
	but 8 in the real input.

	The idea is to hash all the individual towels and then build the towel arrangement
	one towel at a time (recursively). The exit condition is the pointer reaching the end of the arrangement
	"""

	if pointer >= len(arrangement):
		return 1

	else:
		if pointer + max_len > len(arrangement):
			endpoint = len(arrangement)

		else:
			endpoint = pointer + max_len

		for i in range(pointer, endpoint):
			if towels.get(arrangement[pointer:i + 1]):
				sequences += is_possible(arrangement, i + 1)

	return sequences


with open('input.txt') as f:
	REAL_INPUT = f.read()

part_A = 0
part_B = 0

towels, arrangements = parse_input(REAL_INPUT)

for arrangement in arrangements:
	sq = is_possible(arrangement)
	part_B += sq
	if sq:
		part_A += 1

print(f'{part_A=}')
print(f'{part_B=}')
