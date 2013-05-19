from ast import *
from ast import dump as dumpAST, fix_missing_locations, iter_fields, parse as parseAST
from symbol_table import ALL_SYMBOLS

if __package__=="pystick":
	from pystick.commonast import *
	from pystick.util import *
else:
	import sys
	from os.path import abspath, dirname, pardir, join as path_join
	sys.path.append(abspath(path_join(dirname(__file__),pardir,pardir)))
	from commonast import *
	from util import *


class Variable(object):
	def __init__(self, name):
		self.name = name
	
	def __str__(self):
		return self.name

	def is_const(self):
		return False

class SymbolicExprBase(object):
	def __init__(self, val):
		self.val = val
	
	def __str__(self):
		return str(self.val)

	def is_const(self):
		return True

class SymbolicExpr(object):
	def __init__(self, left, op, right=None):
		self.left = left
		self.op = op
		self.op_name = op.__class__.__name__
		self.op_str = ALL_SYMBOLS[type(op)]
		self.right = right
	
	def __str__(self):
		if self.right is not None:
			return "({0} {1} {2})".format(str(self.left),self.op_str,str(self.right))
		else:
			return "({0} {1})".format(self.op_str,str(self.left))
	
	def negate(self):
		return SymbolicExpr(self,Not())

	def is_const(self):
		left_is_const,right_is_const = True,True
		if type(self.left) is SymbolicExpr:
			left_is_const = self.left.is_const()
		if self.right and type(self.right) is SymbolicExpr:
			right_is_const = self.right.is_const()
		return left_is_const and right_is_const

class Eval(object):
	const_types = [int,float,bool]
	
	def __init__(self, env, symbolic):
		self.state = env
		self.env = __builtins__
		self.env.update(env)
		self.symbolic = symbolic
	
	def eval(self, node):
		if type(node) is Name:
			id = node.id
			return self.symbolic[id] if id in self.symbolic else self.env[id]
		elif type(node) is Num:
			return node.n
		elif type(node) is Str:
			return node.s
		else:
			eval_func = Eval.function_dict[type(node)]
			return eval_func(self,node)

	def eval_BinOp(self, node):
		global all_linear

		left = self.eval(node.left)
		right = self.eval(node.right)
		
		left_is_const = self.is_constant(left)
		right_is_const = self.is_constant(right)

		if left_is_const and right_is_const:
			return eval_concretely(node,self.env)
		else:
			if not left_is_const and not right_is_const:
				all_linear = False
			return SymbolicExpr(left,node.op,right)

	def eval_Compare(self, node):
		left = self.eval(node.left)
		right = self.eval(node.comparators[0])
		return SymbolicExpr(left,node.ops[0],right)

	def eval_BoolOp(self, node):
		values = [self.eval(val) for val in node.values]
		left = values[0]
		expr = SymbolicExpr(values[0],node.op,values[1])
		for value in values[2:]:
			expr = SymbolicExpr(expr,node.op,value)
		return expr

	def eval_UnaryOp(self, node):
		global all_linear

		operand = self.eval(node.operand)

		if self.is_constant(operand):
			return eval_concretely(node,self.env)
		else:
			return SymbolicExpr(operand,node.op)

	def is_constant(self, expr):
		expr_type = type(expr)
		return expr_type in Eval.const_types

Eval.function_dict = {
		BinOp: Eval.eval_BinOp,
		Compare: Eval.eval_Compare,
		BoolOp: Eval.eval_BoolOp,
		UnaryOp: Eval.eval_UnaryOp
		}

def eval_concretely(test, line_state):
	test = Module(body=[Assign(targets=[Name(id="__test_cond_result", ctx=Store())], value=test)])
	fix_missing_locations(test)
	code = compile(test,"<string>","exec")
	exec code in line_state
	return line_state["__test_cond_result"]

def eval(node, env, symbolic):
	evaluate = Eval(env,symbolic)
	return evaluate.eval(node)
