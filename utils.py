def pprint(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pprint(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))