from ast import Assign, Attribute, Compare, comprehension, DictComp, ExceptHandler, FunctionDef, IfExp, In, Index, List, Load, Name, NodeTransformer, Store, Str, Subscript, Tuple
from ast import copy_location, dump as dumpAST, fix_missing_locations, increment_lineno, iter_fields, parse as parseAST

if __package__=="pystick":
	from pystick.commonast import *
	from pystick.util import *
else:
	import sys
	from os.path import abspath, dirname, pardir, join as path_join
	sys.path.append(abspath(path_join(dirname(__file__),pardir,pardir)))
	from commonast import *
	from util import *

#TODO Work on enabling scope tracking for while-else, for-else, try-else, and try-finally

class Variable(object):
	def __init__(self, name):
		self.name = name.name if isinstance(name,Variable) else name

	def __eq__(self, other):
		return self.name==other.name

	def __hash__(self):
		return hash(self.name)
	
	def emit(self):
		return Log.log(self.name,Name(id=self.name,ctx=Load()))

class ScopeVariable(Variable):
	def __init__(self,name):
		super(ScopeVariable,self).__init__(name)
	
	def emit(self):
		assign = IfExp(test=Compare(left=Str(s=self.name), ops=[In()], comparators=[Call(func=Name(id="dir",ctx=Load()))]), body=Name(id=self.name, ctx=Load()), orelse=Call(func=Name(id='Void', ctx=Load())))
		return Log.log(self.name,assign)

class Log(object):
	log_dict = "trace"
	section_name = None
	sections = []

	@staticmethod
	def __fromkeys(keys, arg=None):
		if arg:
			return Call(func=Attribute(value=Name(id='dict', ctx=Load()), attr='fromkeys', ctx=Load()), args=[List(elts=keys, ctx=Load()),arg])
		else:
			return Call(func=Attribute(value=Name(id='dict', ctx=Load()), attr='fromkeys', ctx=Load()), args=[List(elts=keys, ctx=Load())])

	@staticmethod
	def init(vars):
		node = Name(id=Log.log_dict, ctx=Store())
		var_strs = [Str(s=var.name) for var in vars]
		void = Call(func=Name(id='Void', ctx=Load()))
		return [Assign(targets=[node], value=DictComp(key=Name(id='__key', ctx=Load()), value=Log.__fromkeys(var_strs,void), generators=[comprehension(target=Name(id='__key', ctx=Store()), iter=Log.__fromkeys(Log.sections))]))]

	@staticmethod
	def emit(section, lineno, vars, rettype=None):
		logging = Log.__start(section,lineno)
		logging.extend(Log.__log_vars(vars))
		if rettype:
			logging.extend(Log.__log_return(rettype))
		logging.extend(Log.__end(section,lineno))
		return logging

	@staticmethod
	def __start(section, lineno):
		Log.section_name = Tuple(elts=[Str(s=section),Num(n=lineno)], ctx=Load())
		Log.sections.append(Log.section_name)
		return []

	@staticmethod
	def __log_vars(vars):
		logging = []
		for var in vars:
			logging.append(var.emit())
		return logging

	@staticmethod
	def __log_return(rettype):
		return [Log.log("return",Call(func=Name(id="type",ctx=Load()),args=[rettype]))]

	@staticmethod
	def __end(section, lineno):
		Log.section_name = None
		return []

	@staticmethod
	def log(name, node):
		return Assign(targets=[Subscript(value=Subscript(value=Name(id=Log.log_dict, ctx=Load()), slice=Index(value=Log.section_name), ctx=Load()), slice=Index(value=Str(s=name)), ctx=Store())], value=node)


class Instrument(NodeTransformer):
	def visit_Module(self, node):
		self.generic_visit(node)
		node.body = Log.init(self.vars) + node.body
		return node

	def visit_FunctionDef(self, node):
		self.func = node.name
		self.scope = set() #Tracks all variables in scope at the current time
		self.params = []   #Contains function's parameter names
		self.body = set()  #Tracks the variables in scope in a block
		self.vars = set()  #Tracks all variables defined throughout the function
		self.returns = False

		self.generic_visit(node)
		
		new_body = Log.emit("Enter",node.lineno,self.params)
		new_body += node.body

		func_end = node_line_end(node)
		if not self.returns:
			new_body.extend(Log.emit("Exit",func_end,self.scope,Void.emit()))
		
		node.body = new_body
		return node

	def visit_Assign(self, node):
		vars = {Variable(var.id) for var in node.targets if type(var) is Name}

		self.vars.update(vars)
		self.scope.update(vars)
		self.generic_visit(node)
		return node

	def visit_Delete(self, node):
		to_delete = [Variable(var.id) for var in node.targets if type(var) is Name]
		for var in to_delete:
			self.scope.remove(var)
		self.generic_visit(node)
		return node

	def visit_For(self, node):
		prior = self.scope.copy()

		if isinstance(node.target,Name):
			self.scope.add(Variable(node.target.id))
			self.vars.add(Variable(node.target.id))
		if not self.returns:
			new_body = Log.emit("Loop",node.lineno,self.scope)

		self.generic_visit(node)
		self.returns = False
		
		node.body = new_body + node.body
		new_vars = self.scope - prior
		new_vars = {ScopeVariable(var) for var in new_vars}
		self.scope = prior | new_vars
		return node

	def visit_If(self, node):
		returns = self.returns

		prior = self.scope.copy()
		orelse,node.orelse = node.orelse,[]

		self.generic_visit(node)
		if_returns,self.returns = self.returns,returns
		node.orelse = self.visit_orelse(orelse,prior)
		orelse_returns,self.returns = self.returns,returns
		self.returns = if_returns and orelse_returns

		self.body.update(self.scope - prior)
		self.body = {ScopeVariable(var) for var in self.body}
		self.scope = prior | self.body
		self.body = set()
		return node

	def visit_Return(self, node):
		if self.returns:
			return node
		else:
			self.returns = True
			self.generic_visit(node)
			new_body = Log.emit("Exit",node.lineno,self.scope,node.value)
			new_body.append(node)
			return new_body
	
	def visit_TryExcept(self, node):
		prior = self.scope[:]
		
		self.generic_visit(node)
		
		new_vars = list(set(self.scope) - set(prior))
		new_vars = [ScopeVariable(var) for var in new_vars]
		self.scope = prior[:] + new_vars[:]
		
		return node

	def visit_While(self, node):
		prior = self.scope.copy()

		new_body = []
		if not self.returns:
			new_body = Log.emit("Loop",node.lineno,self.scope)

		self.generic_visit(node)
		self.returns = False
		
		node.body = new_body + node.body
		new_vars = self.scope - prior
		new_vars = {ScopeVariable(var) for var in new_vars}
		self.scope = prior | new_vars
		return node
	
	def visit_With(self, node):
		prior = self.scope.copy()
		
		self.vars.add(Variable(node.optional_vars.id))
		self.scope.add(Variable(node.optional_vars.id))

		self.generic_visit(node)

		new_vars = self.scope - prior
		new_vars = {ScopeVariable(var) for var in new_vars}
		self.scope = prior | new_vars
		return node

	def visit_arguments(self, node):
		params = [Variable(var.id) for var in node.args]
		if node.vararg:
			params.append(Variable(node.vararg))
		if node.kwarg:
			params.append(Variable(node.kwarg))

		self.vars.update(params)
		self.scope.update(params)
		self.params += params
		return node
	
	def visit_orelse(self, node, prior):
		self.body.update(self.scope - prior)
		self.scope = prior.copy()
		
		result = []
		for code in node:
			returned = self.visit(code)
			if type(returned) is list:
				result += returned
			else:
				result.append(returned)
		return result

def log(program_text, func, input_list):
	program = parseAST(program_text)
	program.body = [node for node in program.body if type(node) is FunctionDef and node.name==func.func_name]
	func_args = func.func_code.co_varnames[:func.func_code.co_argcount]

	instrumented = Instrument().visit(program)

	trace = []

	if input_list:
		for inputs in input_list:
			env = execute_func(instrumented,func,inputs)
			trace.append(env[Log.log_dict])
	else:
		env = execute_func(instrumented,func,{})
		trace.append(env[Log.log_dict])
	
	return trace
