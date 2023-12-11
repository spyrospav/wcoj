class Relation:
    def __init__(self, name, attributes, tuples):
        self.name = name
        self.attributes = attributes
        if tuples is None:
            self.tuples = []
        else:
            self.tuples = tuples
    
    def __str__(self):
        return self.name + ': ' + str(self.tuples)
    
    def add_tuple(self, tuple):
        self.tuples.append(tuple)

    def add_tuples(self, tuples):
        self.tuples.extend(tuples)
    
    def get_tuples(self):
        return self.tuples
    
    def get_attributes(self):
        return self.attributes
    
    def get_name(self):
        return self.name
    
    def project(self, attribute):
        return [t[attribute] for t in self.tuples]
    
    def select(self, attribute, value):
        t = [t for t in self.tuples if t[attribute] == value]
        return t
