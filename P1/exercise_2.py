# Exercise 2 Template

# Do not modify the file name or function header

# Adds e to mylist and returns the resulting list
def list_add(mylist, e):
	# Your code here
	if e is None:
		raise TypeError ("El elemento e es nulo")
	else:
		mylist.append(e)
		return mylist


# Removes the first occurrence of e in mylist and returns the resulting list 
def list_del(mylist, e):
	# Your code here
	if e is None:
		raise TypeError ("El elemento e es nulo")
	elif not mylist:
		raise TypeError("La lista esta vacia")
	else:
		mylist.remove(e)
		return mylist

# Adds the tuple t (value, key) to mydict and returns the resulting dictionary
def dict_add(mydict, t):
	# Your code here
	if t is None:
		raise TypeError ("El elemento t es nulo")
	elif not type(t) is tuple:
		raise TypeError ("t no es una tupla")
	else:
		mydict[t[0]]= t[1]
		return mydict