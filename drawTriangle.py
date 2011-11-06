#!/usr/bin/python

def main():
	drawTriangle(10)


def drawTriangle(height):
	'''
	Print an ascii triangle
	'''
	
	line = ['.'] * height
	base = ['X'] * height
	for i in range(height):
		j = (i * -1) - 1
		rightHalf = line[:]
		rightHalf[j] = 'X'
		leftHalf = line[:]
		leftHalf[i] = 'X'
		if i == (height - 1):
			print base, base
		else:
			print rightHalf, leftHalf
	
if __name__ == '__main__':
	main()