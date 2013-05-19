
class Range(object):
	def __init__(self, var, min_val, max_val):
		self.var = var
		self.min_val = min_val
		self.max_val = max_val
	
	def __str__(self):
		return "{0} <= {1} <= {2}".format(self.min_val,self.var,self.max_val)

class Undef(Range):
	def __init__(self, var):
		Range.__init__(self,var,None,None)

	def __str__(self):
		return "{0} is undefined at this point.".format(self.var)

class Const(Range):
	def __init__(self, var, val):
		Range.__init__(self,var,val,None)
	
	def __str__(self):
		return "{0} == {1}".format(self.var,self.min_val)


def run_funcs(func_list, args):
	results = {}
	for func in func_list:
		try:
			results[func] = func(*args)
		except KeyboardInterrupt:
			raise
		except:
			pass
	return results

