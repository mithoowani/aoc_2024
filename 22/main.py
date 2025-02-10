import numpy as np
from collections import defaultdict

TEST_INPUT = """1
2
3
2024"""

with open('input.txt', 'r') as f:
	REAL_INPUT = f.read()

nums = [int(num) for num in REAL_INPUT.split('\n')]

hashmap = defaultdict(list)

part_A = 0

for num in nums:
	# this ensures that that only the first encountered "difference" window is hashed per monkey
	seen_sequence = {}

	sell_prices = []
	for _ in range(2000):
		sell_prices.append(num % 10)  # for Part B, only need the last digit of the pseudo-random sequence
		num = ((num * 64) ^ num) % 16777216
		num = (int(num / 32) ^ num) % 16777216
		num = ((num * 2048) ^ num) % 16777216

	part_A += num

	# generates 4-digit "difference" windows with their corresponding sell price for one particular monkey
	# e.g. (-9, 4, 3, 1), 2
	diffs = np.array(list(reversed(sell_prices[1:]))) - np.array(list(reversed(sell_prices[:-1])))
	diffs = diffs[::-1]
	windows = ((tuple([diff for diff in diffs[i:i + 4]]), sell_prices[i + 4]) for i in range(0, len(diffs) - 3))

	# hashmap stores all difference windows seen (across all monkeys) and a list of corresponding sell prices
	for key, value in windows:
		if not seen_sequence.get(key):
			hashmap[key].append(value)
			seen_sequence[key] = True

prices = [sum(values) for values in hashmap.values()]
prices.sort(reverse=True)
part_B = prices[0]  # best achievable price across all monkeys
print(f'{part_A=}')
print(f'{part_B=}')
