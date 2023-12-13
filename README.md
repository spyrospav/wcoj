# CIS 6500 - Advanced Databases

## Final Project

This project is an implementation of the Hash-Trie Worst Case Optimal Join (WCOJ) algorithm from the paper *[Adopting Worst-Case Optimal Joins in Relational Database Systems](https://db.in.tum.de/~freitag/papers/p1891-freitag.pdf)*.

## Structure

In order to avoid writing a full SQL parser + Database, we opted to write a imple `db.py` file that contains a `Relation` class to simulate a simple relational table.

We define some helping classes in `utils.py`. More specifically, we implement a `HashTrie` structure supporting all the operations for the trie iterators described in the original paper. 

The join algorithms are implemented in `wcoj.py`. We have a generic `WCOJ` class to initialize the joins, as well as `NaiveWCOJ` and `HashTrieWCOJ` classes that inherit from the generic one and implement the general/naive WCOJ and the Hash-Trie WCOJ respectively.

Finally, we have a `test.py` file to act as a unit tester for these joins.

## Challenges

The original paper describes various optimizations like *singleton pruning* and *lazy child expansion*, which would require careful and challenging implementations. Therefore, they are not implemented.

I was not able to run large experiments to showcase the difference between the two algorithms. The implementation of the evaluation would consist of "compiling" some graph queries from the original paper to the relational table format implemented in `dp.py` and then run the different algorithms and measure time (e.g. with `timeit`).