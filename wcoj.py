from db import Relation

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