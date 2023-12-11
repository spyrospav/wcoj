from db import Relation
import mmh3
import math
from utils import *

class WCOJ:

    def __init__(self, R, fileout = './out/example.txt'):

        self.R = R
        self.V, self.E = [], {}

        # Find all attributes
        for r in R:
            a = r.get_attributes()
            self.V.extend(a)
            self.E[r.get_name()] = a

        self.V = sorted(list(set(self.V)))

        # Open output file
        self.fileout = open(fileout, 'w')

class NaiveWCOJ(WCOJ):

    def enumerate(self, i : int, R : list[Relation]):

        if i <= len(self.V):
            v = self.V[i-1]

            # Relations participating in the current join
            R_join = [Rj for Rj in R if v in self.E[Rj.get_name()]]
            
            # Relations unaffected by the current join
            R_other = [Rj for Rj in R if v not in self.E[Rj.get_name()]]

            # Key values appearing in all joined relations
            keys = set(R_join[0].project(v))

            for Rj in R_join[1:]:
                keys.intersection(set(Rj.project(v)))
            
            # For each key value, recursively enumerate matching tuples
            for ki in keys:
                R_next = R_other.copy()
                skip = False

                for Rj in R_join:
                    matching_tuples = Rj.select(v, ki)
                    if matching_tuples == []:
                        skip = True
                        break
                    R_next.append(
                        Relation(
                            Rj.get_name(), 
                            Rj.get_attributes(), 
                            matching_tuples)
                    )
                
                # If no matching tuples, skip
                if skip:
                    continue
                # Recursively enumerate matching tuples
                self.enumerate(i + 1, R_next)

        else:
            # Produce result tuples
            self.produce(R)

    def produce(self, result):
        
        ret = {}

        for r in result:
            for t in r.get_tuples():
                for k, v in t.items():
                    if k not in ret:
                        ret[k] = v

        # Write result to output file
        self.fileout.write(str(ret) + '\n')

class HashTrieWCOJ(WCOJ):

    def __init__(self, *args, **kwargs):

        self.hash_tries = {}
        super().__init__(*args, **kwargs)

    def build(self):

        # Build hash tries for each relation
        for r in self.R:
            self.hash_tries[r.get_name()] = self._build(
                r.get_attributes(),
                1, 
                r.get_tuples()
            )
            
        return self.hash_tries

    def _build(self, E, i, L):

        if i <= len(E):
            
            sizeL = math.ceil(1.25*len(L))
            v = E[i-1]
            M = {}

            # Build outer hash table
            while L != []:
                t = L.pop()
                hash = mmh3.hash(str(t[v]), False) % sizeL
                if hash not in M:
                    M[hash] = [t]
                else:
                    M[hash].append(t)
                    
            # Build nested hash tables
            for k, v in M.items():
                L_next = v
                M_next = self._build(E, i + 1, L_next)
                M[k] = M_next

            return M
        else:
            return L

    def enumerate(self):
        return self._enumerate(1)
    
    def _enumerate(self, i : int):

        if i <= len(self.V):
            v = self.V[i-1]
            
            # Select participating iterators
            I_join = [self.hash_tries[Rj.get_name()] for Rj in self.R if v in self.E[Rj.get_name()]]
            I_other = [self.hash_tries[Rj.get_name()] for Rj in self.R if v not in self.E[Rj.get_name()]]
            
            # Select smallest hash table
            I_scan = argmin_length(I_join)

            while I_scan != []:
                # Find hash in remaining hash tables

                # Move to the next trie level

                # Recursively enumerate matching tuples
                self._enumerate(i + 1)

                # Move back to the current trie level
        else:
            # All iterators point to tuple chains
            return