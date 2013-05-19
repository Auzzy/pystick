from copy import deepcopy
from  os.path import splitext
from ast import Add, Assign, AugAssign, Del, Delete, Expr, FunctionDef, Index, keyword, Load, Name, Num, Return, Store, Str, Subscript, Tuple, While
from ast import dump as dumpAST, fix_missing_locations, iter_fields, NodeTransformer, NodeVisitor, parse as parseAST
import ast

if __package__=="pystick":
	from pystick.commonast import *
	from pystick.util import *
else:
	import sys
	from os.path import abspath, dirname, pardir, join as path_join
	sys.path.append(abspath(path_join(dirname(__file__),pardir,pardir)))
	from commonast import *
	from util import *

#TODO: Note that this does not currently instrument anything to do with lists or dictionaries. To do this, I will need to watch the functions called in the Call node.

def generate_injected_funcs():
	import funcs
	funcs_src = "{0}.py".format(splitext(funcs.__file__)[0])
	tree_str = open(funcs_src,'r').read()
	del funcs
	tree = parseAST(tree_str)
	return tree.body

class Environment(object):
	name = "__env_dict"
	lineno = "__env_lineno"
	iter_num = "__env_iter_num"
	update_func = "__env_update"
	init_loop_func = "__env_init_loop"
	update_loop_func = "__env_update_loop"
	cleanup_loop_func = "__env_cleanup_loop"
	complete_scope_func = "__env_complete_scope"
	print_func = "__env_print"

	def __init__(self, lineno):
		self.lineno = lineno
		self.loop_update = None

	#int -> list[ast.Assign]
	def init(self, lineno, args):
		init_call = Assign(targets=[Subscript(value=Name(id=Environment.name,ctx=Load()), slice=Index(value=Num(n=lineno)), ctx=Store())], value=Dict())
		param_init = self.assign(lineno,args)
		self.lineno = lineno+1
		return [init_call] + param_init

	#int, list[str] -> list[ast.Assign]
	def assign(self, lineno, vars, loop=False):
		if not isinstance(vars,list):
			vars = [vars]
		
		assignment = []
		for var in vars:
			assignment.append(self.__assign_var(lineno,var,loop))
		return assignment

	#int, str -> ast.Assign
	def __assign_var(self, lineno, var, loop=False):
		lineno_key = Subscript(value=Name(id=Environment.name,ctx=Load()), slice=Index(value=Num(n=lineno)), ctx=Load())
		var_key = lineno_key if not loop else Subscript(value=lineno_key, slice=Index(value=Name(id=Environment.iter_num, ctx=Load())), ctx=Load())
		return Assign(targets=[Subscript(value=var_key, slice=Index(value=Str(s=var)), ctx=Store())], value=Name(id=var,ctx=Load()))

	#int, list[str] -> list[ast.Delete]
	def delete(self, lineno, vars):
		if not isinstance(vars,list):
			vars = [vars]
		
		deletion = []
		for var in vars:
			deletion.append(self.__delete_var(lineno,var))
		return deletion
	
	#int, str -> ast.Delete
	def __delete_var(self, lineno, var):
		return Delete(targets=[Subscript(value=Subscript(value=Name(id=Environment.name,ctx=Load()), slice=Index(value=Num(n=lineno)), ctx=Load()), slice=Index(value=Str(s=var)), ctx=Del())])

	def init_loop(self, loop_start):
		return Expr(value=Call(func=Name(id=Environment.init_loop_func, ctx=Load()), args=[Num(n=loop_start)]))

	#int, int, int -> ast.Expr
	def update_loop(self, lineno, loop_start, loop_end):
		update_call = Expr(value=Call(func=Name(id=Environment.update_loop_func, ctx=Load()), args=[Num(n=self.lineno), Num(n=lineno), Num(n=loop_start), Num(n=loop_end), Name(id=Environment.iter_num, ctx=Load())]))
		self.lineno = lineno+1
		return update_call

	#int, str -> list[ast.AST]
	def end_loop(self, lineno, loop_start):
		loop = [self.update(lineno)]
		cleanup = Expr(value=Call(func=Name(id=Environment.cleanup_loop_func, ctx=Load()), args=[Num(n=lineno), Num(n=1), Name(id=Environment.iter_num, ctx=Load())]))
		loop.append(cleanup)
		
		delete = Delete(targets=[Name(id=Environment.iter_num, ctx=Del())])
		loop.append(delete)
		
		return loop
	
	def generate_try_body(self, orig_body, after_body):
		self.lineno = orig_body[0].lineno
		updated_body = []
		for expr in orig_body:
			updated_body.append(expr)
			if self.lineno<=expr.lineno:
				updated_body.append(self.update(expr.lineno))



		new_body = []
		after_index,updated_index = 0,0
		while after_body[after_index:] and updated_body[updated_index:]:
			after,updated = after_body[after_index],updated_body[updated_index]

			if after==updated:
				new_body.append(after)
				after_index += 1
				updated_index += 1
			else:
				if after in orig_body:
					new_body.append(updated)
					updated_index += 1
				elif updated in orig_body:
					new_body.append(after)
					after_index += 1
				else:
					new_body.append(after)
					after_index += 1
					updated_index += 1

		new_body.extend(after_body[after_index:])
		new_body.extend(updated_body[updated_index:])
		return new_body

	#int -> ast.Expr
	def update(self, lineno):
		call = Expr(value=Call(func=Name(id=Environment.update_func, ctx=Load()), args=[Num(n=self.lineno), Num(n=lineno)]))
		self.lineno = lineno+1
		return call
	
	#int -> ast.Expr
	def complete_scope(self, start, end):
		return Expr(value=Call(func=Name(id=Environment.complete_scope_func, ctx=Load()), args=[Num(n=start), Num(n=end)]))


class Instrument(NodeTransformer):
	def __init__(self):
		self.cur = 1

	def generic_visit(self, node):
		try:
			self.cur = node.lineno
		except AttributeError:
			pass
		super(Instrument,self).generic_visit(node)
		return node

	def visit_Module(self, node):
		self.generic_visit(node)
		node.body = generate_injected_funcs() + node.body
		return node

	def visit_FunctionDef(self, node):
		lineno = node.lineno
		self.func_start,self.func_end = node.lineno,FindEnd(node).end
		self.env = Environment(lineno)
		self.env_assign = self.env.assign
		self.env_update = self.env.update

		args = self.__get_func_args(node.args)
		env_init = self.env.init(lineno,args)

		self.generic_visit(node)
	
		node.body = env_init + node.body
		if not isinstance(node.body[-1],Return):
			if self.env.lineno<self.cur+1:
				node.body.append(self.env.update(self.cur))
			node.body.append(self.env.complete_scope(self.func_start,self.func_end))

		return node

	def __get_func_args(self, arguments):
		arg_names = [var.id for var in arguments.args]
		if arguments.vararg:
			arg_names.append(arguments.vararg)
		if arguments.kwarg:
			arg_names.append(arguments.kwarg)
		return arg_names
		
	
	def visit_Assign(self, node):
		#This line assumes there is a single target. Mishandles code like the following: z = x,y = 1,2
		target = node.targets[0]
		if isinstance(target,Name):
			var_names = [target.id]
		elif isinstance(target,Tuple):
			var_names = [var.id for var in target.elts]
		elif isinstance(target,Subscript):
			var_names = [self.__get_sequence_name(target)]
		else:
			var_names = []

		return self.__visit_assign(node,var_names)

	def visit_AugAssign(self, node):
		return self.__visit_assign(node,[node.target.id])

	def visit_Delete(self, node):
		lineno = node.lineno
		log = [self.env_update(lineno)] if self.env.lineno<=lineno else []
		targets = node.targets

		var_names = [var.id for var in targets]
		log.extend(self.env.delete(lineno,var_names))

		self.generic_visit(node)

		log.insert(0,node)
		return log


	def visit_If(self, node):
		orelse,node.orelse = node.orelse,[]
		update_if = self.env_update(node.lineno)

		self.generic_visit(node)
		
		if self.env.lineno<=self.cur:
			node.body.append(self.env_update(self.cur))

		node.orelse = self.__visit_branch(orelse)

		if self.env.lineno<=self.cur:
			node.orelse.append(self.env_update(self.cur))
		return [update_if,node]
	
	#For the time being, will assume user is providing 1 target and is not calling enumerate() on the iterable
	def visit_For(self, node):
		def inject_counter(node):
			target = node.target
			node.target = Tuple(elts=[Name(id=Environment.iter_num, ctx=Store()),target], ctx=Store())
			node.iter = Call(func=Name(id='enumerate', ctx=Load()), args=[node.iter, Num(n=1)])
			return target
		
		return self.__visit_loop(node,inject_counter)

	def visit_While(self, node):
		return self.__visit_loop(node,lambda node: None)

	def visit_TryExcept(self, node):
		handlers,node.handlers = node.handlers,[]
		body = node.body[:]
		update_try = self.env_update(node.lineno)

		self.generic_visit(node)
		
		node = fix_missing_locations(node)
		node.body = self.env.generate_try_body(body,node.body)
		
		node.handlers = self.__visit_branch(handlers)
		
		return [update_try,node]
	
	def visit_ExceptHandler(self, node):
		new_body = [self.env_update(node.lineno)]

		self.generic_visit(node)
		
		if node.name is not None:
			new_body.extend(self.env.assign(node.lineno,node.name.id))
		node.body = new_body + node.body
		if self.env.lineno<=self.cur:
			node.body.append(self.env_update(self.cur))
		return node
	
	def visit_Return(self, node):
		lineno = node.lineno
		new_nodes = [self.env_update(lineno)] if self.env.lineno<=lineno else []
		new_nodes.append(self.env.complete_scope(self.func_start,self.func_end))
		new_nodes.append(node)
		return new_nodes


	def __visit_assign(self, node, var_names):
		lineno = node.lineno
		log = [self.env_update(lineno)] if self.env.lineno<=lineno else []
		log.extend(self.env_assign(lineno,var_names))
		
		self.generic_visit(node)
		
		log.insert(0,node)
		return log

	def __visit_branch(self, node_list):
		result = []
		for node in node_list:
			returned = self.visit(node)
			result += returned if isinstance(returned,list) else [returned]
		return result

	def __visit_loop(self, node, inject_counter):
		loop_start,loop_end = node.lineno,FindEnd(node).end + 1
		target = inject_counter(node)
		update_call = self.env.update_loop(loop_start,loop_start,loop_end)
		
		self.__visit_loop_body(node,loop_end)
		
		node.body.insert(0,update_call)
		
		if self.env.lineno<=self.cur:
			node.body.append(self.env.update_loop(self.cur,loop_start,loop_end))
		
		if isinstance(node,While):
			node.body.append(AugAssign(target=Name(id=Environment.iter_num, ctx=Store()), value=Num(n=1), op=Add()))
		else:
			node.body[1:1] = self.env.assign(loop_start,[target.id],loop=True)
		
		new_nodes = [self.env.init_loop(loop_start),
				Assign(targets=[Name(id=Environment.iter_num, ctx=Store())], value=Num(n=1)),
				node]
		new_nodes.extend(self.env.end_loop(loop_end,loop_start))
		return new_nodes
	
	def __visit_loop_body(self, node, loop_end):
		self.env_assign = lambda *args: self.env.assign(*args,loop=True)
		self.env_update = lambda node_lineno: self.env.update_loop(node_lineno,node.lineno,loop_end)
		self.generic_visit(node)
		self.env_assign = self.env.assign
		self.env_update = self.env.update


class FindEnd(NodeVisitor):
	def __init__(self, node):
		node = ast.fix_missing_locations(node)
		self.visit(node)

	def generic_visit(self, node):
		try:
			self.end = node.lineno
		except AttributeError:
			pass
		super(FindEnd,self).generic_visit(node)

def eval(program, func, inputs={}):
	tree = Instrument().visit(deepcopy(program))

	env = execute_func(tree,func,inputs)

	return env["__env_dict"]
