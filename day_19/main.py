from pprint import pprint
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
def is_possible(word, pointer=0, max_len=8, sequences=0):
	if pointer >= len(word):
		return 1

	else:
		if pointer + max_len > len(word):
			endpoint = len(word)

		else:
			endpoint = pointer + max_len

		for i in range(pointer, endpoint):
			# print(word[pointer:i + 1])
			if l.get(word[pointer:i + 1]):
				sequences += is_possible(word, i + 1)

	return sequences


# return sequences

# if valid:
# 	sequences += 1
# sequence.append(word[pointer:i + 1])


with open('input.txt') as f:
	REAL_INPUT = f.read()

count = 0
total_sequences = 0

l, w = parse_input(REAL_INPUT)

for word in w:
	sq = is_possible(word)
	total_sequences += sq
	if sq:
		count += 1

# print(f'{word} is VALID')
# print(sequences)
# else:
# 	print(f'{word}')

print(f'{count=}')
print(f'{total_sequences=}')
