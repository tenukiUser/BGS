# BGS project by La Branche (https://discord.gg/AD7H4jX)
# Developpers : Antoine D., Kernel
# typetools module -- classes and functions for built-in types

def delete_items(L:list,iterable:list,in_place=True):
	"""
	Delete items from L with indexes given by iterable of length n.
	If in_place is set to False, returns a new list.
	(this is an extension to the pop method.)
	"""
	n = len(iterable)

	if in_place:
		for i in iterable:
			L[i] = None

		for j in range(n):
			L.remove(None)

		return None

	else:
		Lcopy = L.copy()
		for i in iterable:
			Lcopy[i] = None

		for j in range(n):
			Lcopy.remove(None)

		return Lcopy




