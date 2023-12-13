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
        
        self.fileout = fileout

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

        # Open output file
        fileout = open(self.fileout, 'a')
        # Write result to output file
        fileout.write(str(ret) + '\n')
        # Close output file
        fileout.close()

class HashTrieWCOJ(WCOJ):

    def __init__(self, *args, **kwargs):

        self.hash_tries = []
        super().__init__(*args, **kwargs)

    def build(self):

        # Build hash tries for each relation
        for r in self.R:
            mod = math.ceil(1.25*len(r.get_tuples()))
            node = self._build(r, 1, r.get_tuples(), mod)
            self.hash_tries.append(
                HashTrie(
                    r.get_name(), 
                    r.get_attributes(),
                    mod, 
                    node
                )
            )
            
        return self.hash_tries

    def _build(self, R, i, L, mod):

        E = R.get_attributes()
        if i <= len(E):
            
            v = E[i-1]
            M = HashTrieNode()
            
            # Build outer hash table
            while L != []:
                t = L.pop()
                hash = mmh3.hash(str(t[v]), False) % mod
                M.push(hash, t)
                    
            # Build nested hash tables
            for key, val in M.buckets.items():
                L_next = val.list
                M_next= self._build(R, i + 1, L_next, mod)
                M.buckets[key].next = M_next
                M_next.set_parent(M)
            return M
        else:
            return Leaf(L)

    def enumerate(self):
        return self._enumerate(1)
    
    def _enumerate(self, i : int):

        if i <= len(self.V):
            v = self.V[i-1]
            
            # Select participating iterators
            I_join = [I for I in self.hash_tries if v in I.attributes]
            
            # Select smallest hash table
            I_scan = I_join[0]

            for t in I_scan.iterator.buckets:
                # Find hash in remaining hash tables
                skip = False
                for I in I_join:
                    if I.iterator != I_scan.iterator:
                        if not I.lookup(t):
                            skip = True
                            break
                if skip:
                    continue

                # Move to the next trie level
                for I in I_join:
                    I.move(t)

                # Recursively enumerate matching tuples
                self._enumerate(i + 1)

                # Move back to the current trie level
                for I in I_join:
                    I.up()
        else:
            # All iterators point to tuple chains
            tuple = {}
            check = {}
            save = True
            print("sadas")
            for I in self.hash_tries:
                print(I.iterator.list)
                for t in I.iterator.list:
                    print(t)
                    for k, v in t.items():
                        print(k)
                        if v not in check:
                            check[v] = 1
                            tuple[k] = v
                        else:
                            if check[v] == 2:
                                save = False
                                break
                            else:
                                check[v] = check[v] + 1
                        if not save:
                            break
                    if not save:
                        break
                if not save:
                    break

            if save:
                # Open output file
                fileout = open(self.fileout, 'a')
                # Write result to output file
                fileout.write(str(tuple) + '\n')
                # Close output file
                fileout.close()