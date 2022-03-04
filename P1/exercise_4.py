# Exercise 4 Template
import os
import string

# Do not modify the file name or function header

# Return the size of the file and words ending in 's'
def get_file_info(filename):
	# Your code here
	size = 0
	wordlist = []

	if not type(filename) is str or filename is None:
		raise TypeError("El parametro filename no es una cadena o es nulo")
	elif not os.path.isfile(filename):
		raise OSError("El fichero no existe")
	else:
		size = os.path.getsize(filename)

		with open(filename,'r') as file: 
			for line in file:
				for word in line.split():
					if word[-1:] is 's':
						wordlist.append(word)

		return (size, wordlist)