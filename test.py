from wcoj import NaiveWCOJ, HashTrieWCOJ
from db import Relation
import utils

# Relations R1, R2, R3
R1 = Relation('R1', ['v1', 'v2'], [])
R2 = Relation('R2', ['v2', 'v3'], [])
R3 = Relation('R3', ['v1', 'v3'], [])

# Add these tuples to all the relations (0, 1), (1, 2), (1, 3), (2, 0), (2, 3)
R1.add_tuples([{'v1': 0, 'v2': 1}, {'v1': 1, 'v2': 2}, {'v1': 1, 'v2': 3}, {'v1': 2, 'v2': 0}, {'v1': 2, 'v2': 3}])
R2.add_tuples([{'v2': 0, 'v3': 1}, {'v2': 1, 'v3': 2}, {'v2': 1, 'v3': 3}, {'v2': 2, 'v3': 0}, {'v2': 2, 'v3': 3}])
R3.add_tuples([{'v3': 0, 'v1': 1}, {'v3': 1, 'v1': 2}, {'v3': 1, 'v1': 3}, {'v3': 2, 'v1': 0}, {'v3': 2, 'v1': 3}])

# Naive WCOJ
wcoj = NaiveWCOJ([R1, R2, R3], "out/naive.txt")
wcoj.enumerate(1, [R1, R2, R3])

# HashTrie WCOJ
wcojHash = HashTrieWCOJ([R1, R2, R3], "out/hash_trie.out")
wcojHash.build()
wcojHash.enumerate()