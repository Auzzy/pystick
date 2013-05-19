import sys
from copy import deepcopy

from ast import Call, Expr, keyword, Load, Name, Num
from ast import fix_missing_locations
from commonast import *

class Void(object):
	@staticmethod
	def emit():
		return Call(func=Name(id='Void',ctx=Load()))
	
	def __str__(self):
		return "Void"

	def __repr__(self):
		return "Void()"

	def __eq__(self, other):
		return type(other) is Void

class BlackHole(object):
	def write(self, to_ignore):
		#open("log.txt",'a').write(to_ignore)
		pass
BLACK_HOLE = BlackHole()


def _node_line_end(node):
	try:
		return _node_line_end(node.orelse[-1])
	except:
		try:
			return _node_line_end(node.body[-1])
		except:
			return node.lineno+1

def node_line_end(root):
	root_copy = deepcopy(root)
	fix_missing_locations(root_copy)
	return _node_line_end(root)


# http://mail.python.org/pipermail/python-list/2004-September/282520.html
def all_pairs(seq):
	length = len(seq)
	for i in range(length):
		for j in range(i+1, length):
			yield seq[i], seq[j]

def exec_code(code):
	env = {}
	env["Void"] = Void
	exec code in env
	return env

def silent_exec(code):
	sys.stdout = BLACK_HOLE
	env = exec_code(code)
	sys.stdout = sys.__stdout__

	return env

def transform_input_list(inputs):
	keyword_list = []

	for input in inputs:
		keyword_item = keyword(arg=input, value=Num(n=inputs[input]))
		keyword_list.append(keyword_item)
	
	return keyword_list

def execute_func(tree, func, inputs, silent=True):
	tree_copy = deepcopy(tree)
	input_nodes = transform_input_list(inputs)
	tree_copy.body.append(Expr(value=Call(func=Name(id=func.func_name, ctx=Load()), keywords=input_nodes)))
	fix_missing_locations(tree_copy)
	code = compile(tree_copy,"<string>","exec")
	execute = silent_exec if silent else exec_code
	return execute(code)
