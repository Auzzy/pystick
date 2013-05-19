def test1():
	num = 4+6
	print num
	num2 = 9
	del num
	print num2

def test2(x, y):
	num = 8
	if x != y:
		if 2*x == x+10:
			return y
		else:
			num = 4
	return num

def test3(x):
	num = 1
	num = num+1
	if num+x<8:
		num = 2
	elif num==3:
		num = 4
	else:
		num = 5
		print "HEY"
	num2 = 6

def test4(num, num2):
	if num==3:
		if num2:
			print "here"
		else:
			print "yup"
	else:
		print "HI!"

def test5(num):
	if num==4:
		return 8
	num2 = 0

def test6(x, y):
	num = 8
	if x!=y:
		if 2*x==x+10:
			return y
		else:
			if y==7:
				num = 4
	return num

def test7(x, y):
	z = y
	if x==z:
		if y==x+10:
			print "ERROR"

def test8(x, y):
	if x!=y:
		if 2*x==x+10:
			pass
		else:
			if y==7:
				pass

def test9(x, y):
	if x!=y:
		print "x != y "
		if 2*x==x+10:
			print "2*x == x+10"
		else:
			print "2*x != x+10"
			if y==7:
				print "y == 7"
			else:
				print "y != 7"
	else:
		print "x == y "
