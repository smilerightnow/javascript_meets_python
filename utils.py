

def getKeysDict(dictionary):
	for key, value in dictionary.items():
		yield (key, value)

def getAllKeysDict(dictionary):
	for key, value in dictionary.items():
		yield (key, value)
		if type(value) is dict:
			yield from getAllKeysDict(value)

def between_tuple(x, t):
	if type(x) == tuple:
		return min(t) <= min(x) <= max(t)
	return min(t) <= x <= max(t)

def between_tuples(x, list_t):
	for t in list_t:
		if between_tuple(x,t): return True
	return False
