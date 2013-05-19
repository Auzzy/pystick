def test1(x, y):
	num = 8
	if x != y:
		if 2*x == x+10:
			return y
		else:
			num = 4
	return num

def test2():
	num = 4+6
	print num
	num2 = 9
	del num
	print num2

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

def test4():
	i = 2
	while i<10:
		print i
		i += 2

def test5():
	try:
		temp = 7
		print temp
		print num3
		print
		test = 2
	except NameError,mess:
		num2 = 8
		print
	except TypeError:
		num2 = 7
	print "hi"

def test6(num, num2=12, *num3, **num4):
	del num2
	return num

def test7(num, num2=12, *num3, **num4):
	if num==4:
		return "HI!"
	else:
		pass
	return None

def test8(num, num2):
	if num==3:
		if num2:
			print "here"
		else:
			print "yup"
	else:
		print "HI!"

def test9():
	try:
		try:
			print num
		except NameError,mess:
			print "HERE"
		4/0
	except ZeroDivisionError,mess:
		print "yup!"

def test10(num):
	if num==4:
		return 8
	num2 = 0

def test11(x, y):
	num = 8
	if x!=y:
		if 2*x==x+10:
			return y
		else:
			if y==7:
				num = 4
	return num

def test12(x, y):
	z = y
	if x==z:
		if y==x+10:
			print "ERROR"

def test13(x, y):
	if x!=y:
		if 2*x==x+10:
			pass
		else:
			if y==7:
				pass

def test14(x, y):
	while x<y:
		x = x+1

def test15(x, y):
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
