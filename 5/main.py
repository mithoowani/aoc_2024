import numpy as np
from functools import cmp_to_key

TEST_INPUT = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse_input(puzzle_input: str) -> (np.array, list):
	"""
	Parses puzzle input by separating rules from pages
	:param puzzle_input: string containing all puzzle input
	:return: numpy array containing all rules; list of lists containing pages to validate
	"""
	all_input = puzzle_input.split('\n')
	break_index = all_input.index('')
	rules, pages = all_input[:break_index], all_input[break_index + 1:]

	rules_list = [rule.split('|') for rule in rules]
	rules_array = np.array(rules_list).astype('int64')  # convert rules from str -> int

	pages_list = [page.split(',') for page in pages]
	pages_list = [[int(page) for page in entry] for entry in pages_list]  # convert all values from str -> int

	return rules_array, pages_list


def compare(page1, page2):
	"""
	Custom sort function comparing two pages; if page1 precedes page2 according to ruleset, then returns -1,
	otherwise returns 1.
	:param page1: int
	:param page2: int
	:return: int
	"""
	for rule in rules:
		if rule[0] == page1 and rule[1] == page2:
			return -1
		elif rule[0] == page2 and rule[1] == page1:
			return 1
	return 0


# Test input
# rules, entries = parse_input(TEST_INPUT)

# Real input
with open('input.txt', 'r') as f:
	INPUT = f.read()
rules, entries = parse_input(INPUT)

# PART A and B
all_valid_sum = 0  # Sum of middle pages among correctly sorted entries
all_invalid_sum = 0  # Sum of middle pages among initially incorrectly sorted entries

for entry in entries:
	valid = True
	for page in entry:
		relevant_rules = np.argwhere(rules == page)
		for rule in relevant_rules:
			if rule[1] == 0:  # page has to come before the other one in the relevant rule
				before = page
				after = rules[rule[0], 1]
				if after in entry and entry.index(after) < entry.index(before):
					valid = False
					break
			elif rule[1] == 1:  # page has to come after the other one in the relevant rule
				before = rules[rule[0], 0]
				after = page
				if before in entry and entry.index(after) < entry.index(before):
					valid = False
					break

	if valid:
		all_valid_sum += entry[len(entry) // 2]

	else:  # Part B
		correctly_sorted = sorted(entry, key=cmp_to_key(compare))
		all_invalid_sum += correctly_sorted[len(correctly_sorted) // 2]

print('Part A:', all_valid_sum)
print('Part B:', all_invalid_sum)
