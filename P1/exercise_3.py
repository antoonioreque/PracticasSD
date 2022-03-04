# Exercise 3 Template

# Do not modify the file name or function header

# Retuns a list with the prime numbers in the [a, b] interval
def prime(a, b):
	# Your code here
	primes = []
	if a is None or b is None:
		raise TypeError("A o B son nulos")
	elif not type(a) is int or not type(b) is int:
		raise TypeError("A o B no son enteros")
	else:
		for x in range(a,b+1):		#Ponemos el +1 para que incluya tambien el ultimo numero
			divisor = x-1
			while divisor > 1:
				if x%divisor == 0:
					break
				else:
					divisor-=1
			if divisor == 1:
				primes.append(x)
					
	# ...

	return primes
