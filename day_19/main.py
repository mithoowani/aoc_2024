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

@cache
def is_possible(word, pointer=0, max_len=8):
	# print(word, pointer)
	if pointer >= len(word):
		return True

	else:
		for i in range(pointer, pointer + max_len):
			# print(word[pointer:i + 1])
			if l.get(word[pointer:i + 1]):
				if is_possible(word, i + 1):
					return True

		else:
			return False


with open('input.txt') as f:
	REAL_INPUT = f.read()

count = 0
l, w = parse_input(REAL_INPUT)

for word in w:
	if is_possible(word):
		count += 1
		print(f'{word} is VALID')
	else:
		print(f'{word}')

print(count)
