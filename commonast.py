import ast
from ast import AST, iter_fields, dump

dumpAST = lambda node: dump(node,include_attributes=False)

class Call(ast.Call):
	def __init__(self, **kwargs):

		if "args" not in kwargs:
			kwargs["args"] = []
		if "keywords" not in kwargs:
			kwargs["keywords"] = []
		if "starargs" not in kwargs:
			kwargs["starargs"] = None
		if "kwargs" not in kwargs:
			kwargs["kwargs"] = None
		super(Call,self).__init__(**kwargs)

class Print(ast.Print):
	def __init__(self, **kwargs):
		if "dest" not in kwargs:
			kwargs["dest"] = None
		if "nl" not in kwargs:
			kwargs["nl"] = True
		super(Print,self).__init__(**kwargs)

class Dict(ast.Dict):
	def __init__(self, **kwargs):
		if "keys" not in kwargs:
			kwargs["keys"] = []
		if "values" not in kwargs:
			kwargs["values"] = []
		super(Dict,self).__init__(**kwargs)

class Slice(ast.Slice):
	def __init__(self, **kwargs):
		if "lower" not in kwargs:
			kwargs["lower"] = None
		if "upper" not in kwargs:
			kwargs["upper"] = None
		if "step" not in kwargs:
			kwargs["step"] = None
		super(Slice,self).__init__(**kwargs)

class comprehension(ast.comprehension):
	def __init__(self, **kwargs):
		if "ifs" not in kwargs:
			kwargs["ifs"] = []
		super(comprehension,self).__init__(**kwargs)

def print_tree_info(tree):
	BODY = "body"
	field_dict = dict(iter_fields(tree))
	body_tree = None
	if BODY in field_dict:
		body_tree = field_dict[BODY]
		del field_dict[BODY]

	#FIELDS
	for field in field_dict:
		print field
		if type(field_dict[field]) is list:
			for node in field_dict[field]:
				print dumpAST(node)
				print
		elif type(field_dict[field]) is AST:
			print dumpAST(field_dict[field])
		else:
			print field_dict[field]
		print


	#CHILDREN
	for child in body_tree:
		print dumpAST(child)
		print

