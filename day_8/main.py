TEST_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def parse_input(puzzle_input: str):
	output = dict()
	input_lines = puzzle_input.split('\n')
	n_rows = len(input_lines)
	n_cols = len(input_lines[0])
	for row_num, line in enumerate(input_lines):
		for col_num, cell in enumerate(line):
			if cell.isalnum():
				output[(row_num, col_num)] = cell
	return output, n_rows, n_cols


# Uncomment to work with the test input
# towers, num_rows, num_cols = parse_input(TEST_INPUT)

with open('input.txt') as f:
	REAL_INPUT = f.read()

# num_rows and num_cols are the dimensions of the input grid
towers, num_rows, num_cols = parse_input(REAL_INPUT)

antinodes = dict()
antinodes_b = dict()

letters_lower = 'abcdefghijklmnopqrstuvwxyz'
characters = letters_lower + letters_lower.upper() + '0123456789'

for char in characters:

	# extract locations of all towers with the same character
	relevant_towers = []
	for k, v in towers.items():
		if v == char:
			relevant_towers.append(k)

	# identify all pairs of towers
	for i in relevant_towers:

		# if there is at least one pair of towers, then mark each tower location as an antinode (for part b)
		if len(relevant_towers) > 1:
			antinodes_b[(i[0], i[1])] = 1

		for j in relevant_towers:
			if i != j:
				row_delta = i[0] - j[0]
				col_delta = i[1] - j[1]
				antinode_row, antinode_col = i[0] + row_delta, i[1] + col_delta
				if 0 <= antinode_row < num_rows and 0 <= antinode_col < num_cols:
					antinodes[(antinode_row, antinode_col)] = 1

					# part b code
					while 0 <= antinode_row < num_rows and 0 <= antinode_col < num_cols:
						antinodes_b[(antinode_row, antinode_col)] = 1
						antinode_row += row_delta
						antinode_col += col_delta

print(f'Part A: {len(antinodes)}')
print(f'Part B: {len(antinodes_b)}')
