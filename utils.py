def pprint(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, Bucket):
         if isinstance(value.next, Leaf):
            print('\t' * (indent+1) + str(value.list))
         else:
            pprint(value.next.buckets, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

class Bucket():

   def __init__(self, list = [], next = None):
      self.list = list
      self.next = next

   def push(self, item):
      self.list.append(item)

   def next(self):
      return self.next

class Leaf():

   def __init__(self, list):
      self.list = list
      self.parent = None

   def set_parent(self, parent = None):
      self.parent = parent
   
class HashTrieNode():

   def __init__(self):
      self.buckets = {}
      self.parent = None
      self.current_bucket = None
   
   def push(self, hash, t):
      if hash in self.buckets:
         self.buckets[hash].push(t)
      else:
         self.buckets[hash] = Bucket([t], None)

   def set_parent(self, parent = None):
      self.parent = parent

class HashTrie():

   def __init__(self, name, attributes, size, node = None):
      self.name = name
      self.attributes = attributes
      self.size = size
      self.iterator = node
      
   def up(self):
      if self.iterator.parent:
         self.iterator = self.iterator.parent
   
   def move(self, hash):
      # if isinstance(self.iterator, Bucket):
      self.iterator = self.iterator.buckets[hash].next
   
   def lookup(self, hash):
      if hash in self.iterator.buckets:
         return True
      else:
         return False



