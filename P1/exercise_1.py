# Exercise 1 Template

# Do not modify the file name or function header

# Return the sum of those parameters that contain an even number

def accum(x, y, z):
	# Your code here
    sum = 0
    if  not type(x) is int or not type(y) is int or not type(z) is int:
        raise TypeError("Only integers are allowed")
    else:      
        if x%2== 0:
            sum += x
        if y%2== 0:
            sum += y
        if z%2== 0:
            sum += z
        
        return sum
