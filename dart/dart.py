from random import random,randint,choice as random_item
from ast import Assign, BinOp, Compare, Eq, FunctionDef, Load, Module, Name, Num, NodeTransformer, NodeVisitor, Slice, Store, Subscript
from ast import fix_missing_locations, parse as parseAST

from constraint_solver import get_solutions
from hashdict import *

"""
from pystick.dart.concrete import eval as eval_concrete
from pystick.dart.symbolic import Variable,eval as eval_symbolic
"""

from concrete import eval as eval_concrete
from symbolic import Variable,eval as eval_symbolic

import constraint_solver
MAX_VAL = constraint_solver.MAX_VAL = 10
del constraint_solver

if __package__=="pystick":
	from pystick.commonast import *
else:
	import sys
	from os.path import abspath, dirname, pardir, join as path_join
	sys.path.append(abspath(path_join(dirname(__file__),pardir)))
	from commonast import *


class SymbolicExecutionExit(SystemExit):
	pass

#TODO: Give the ability to generate random function inputs of varying types.
#TODO: Should not have to eval_if. Concrete evaluation should make note of the result.

class Execute(NodeVisitor):
	def __init__(self, env):
		self.env = env
		self.path_constraints = []
		self.branchno = 0

	def visit_Module(self, node):
		self.generic_visit(node)

	def visit_FunctionDef(self, node):
		self.symbolic_memory = {key:Variable(key) for key in self.env[node.lineno]}
		try:
			self.generic_visit(node)
		except SymbolicExecutionExit:
			pass

	def visit_Assign(self, node):
		name = node.targets[0].id
		state = self.env[node.lineno]
		if name in self.symbolic_memory:
			state[name] = self.symbolic_memory[name]
		self.symbolic_memory[name] = eval_symbolic(node.value,state,self.symbolic_memory)
		
		self.generic_visit(node)

	def visit_AugAssign(self, node):
		def AugAssignToAssign(node):
			store_var = node.target
			load_var = Name(id=store_var.id, ctx=Load())
			return Assign(targets=[store_var], value=BinOp(left=load_var, op=node.op, right=node.value))
		
		new_node = AugAssignToAssign(node)
		new_node.lineno = node.lineno
		new_node.col_offset = node.col_offset
		self.visit(new_node)

	def visit_If(self, node):
		test = node.test
		state = self.env[node.lineno]
		then_branch = self.eval_if(test,state)
		expr = eval_symbolic(test,state,self.symbolic_memory)

		if then_branch:
			orelse,node.orelse = node.orelse,[]
			self.path_constraints += [expr]
		else:
			body,node.body = node.body,[]
			self.path_constraints += [expr.negate()]

		self.compare_and_update_stack(then_branch,self.branchno)
		self.branchno += 1

		self.generic_visit(node)
		
		if then_branch:
			node.orelse = orelse
		else:
			node.body = body
	
	def visit_Return(self, node):
		raise SymbolicExecutionExit(0)
	
	def visit_While(self, node):
		test = node.test
		state = self.env[node.lineno]
		iter_num = 1

		loop = self.eval_if(test,state[iter_num])
		expr = eval_symbolic(test,state[iter_num],self.symbolic_memory)

		if not expr.is_const():
			if loop:
				self.path_constraints += [expr]
			else:
				self.path_constraints += [expr.negate()]

			self.compare_and_update_stack(loop,self.branchno)
			self.branchno += 1

		if loop:
			iter_num += 1
			self.generic_visit(node)
			while True:
				loop = iter_num in state
				
				if not expr.is_const():
					self.compare_stack(loop,self.branchno)

				if not loop:
					break
				
				if not expr.is_const():
					self.update_stack(loop,self.branchno)
				expr = eval_symbolic(test,state[iter_num],self.symbolic_memory)
				if not expr.is_const():
					self.path_constraints += [expr]
					self.branchno += 1
				iter_num += 1

				self.generic_visit(node)

	##### HELPERS #####

	def eval_if(self, test, line_state):
		test = Module(body=[Assign(targets=[Name(id="__test_cond_result", ctx=Store())], value=test)])
		fix_missing_locations(test)
		code = compile(test,"<string>","exec")
		exec code in line_state
		return line_state["__test_cond_result"]
	
	# branch_taken will be True when the "then" branch was taken, and False when the "else" branch was taken
	def compare_and_update_stack(self, branch_taken, branchno):
		global stack

		self.compare_stack(branch_taken,branchno)
		self.update_stack(branch_taken,branchno)
	
	def compare_stack(self, branch_taken, branchno):
		global stack,forcing_ok
		
		if branchno<len(stack):
			if stack[branchno]["branch"] ^ branch_taken:
				forcing_ok = False
				raise Exception("Took an unexpected branch.")
			elif branchno==len(stack)-1:
				stack[branchno]["branch"] = branch_taken
				stack[branchno]["done"] = True

	def update_stack(self, branch_taken, branchno):
		global stack

		if branchno>=len(stack):
			stack.append({"branch":branch_taken, "done":False})

def next_unfinished_branch(tried):
	global stack

	for unfinished,branch in reversed(list(enumerate(stack[:tried]))):
		if not branch["done"]:
			return unfinished
	return None

def solve_path_constraints(tried, constraints, scope_vars):
	global stack,directed

	unfinished_index = next_unfinished_branch(tried)
	
	if unfinished_index is not None:
		constraints[unfinished_index] = constraints[unfinished_index].negate()
		stack[unfinished_index]["branch"] = not stack[unfinished_index]["branch"]
		new_solutions = get_solutions(constraints[:unfinished_index+1], scope_vars)

		if new_solutions:
			stack = stack[:unfinished_index+1]
			return new_solutions
		else:
			return solve_path_constraints(unfinished_index,constraints,scope_vars)
	else:
		directed = False
		return None

def filter_inputs(new_solutions, input_vars):
	if new_solutions:
		def new_hashdict(solution):
			return hashdict({var:solution[var] for var in input_vars})
		return {new_hashdict(solution) for solution in new_solutions}

def get_random_val(val_type):
	if val_type is int:
		return randint(0,MAX_VAL)
	elif val_type is float:
		return random()*MAX_VAL

def execute_program(program, user_func, inputs):
	global stack,solutions,path_constraints

	env = eval_concrete(program,user_func,inputs)
	execute = Execute(env)
	execute.visit(program)
	path_constraints[inputs] = list(execute.path_constraints)

	new_solutions = solve_path_constraints(len(stack),execute.path_constraints,execute.symbolic_memory.keys())
	new_solutions = filter_inputs(new_solutions,inputs.keys())

	if directed:
		inputs = random_item(list(new_solutions)) if new_solutions else None
		solutions[inputs] = new_solutions
	else:
		unfinished = [branch for branch in stack if not branch["done"]]
		if unfinished:
			print "At least one branch cannot be taken due to a condition that cannot be completely covered."
		inputs = None
		stack = None
	
	return inputs

def random_inputs(func_args):
	inputs = {var:get_random_val(int) for var in func_args}
	return hashdict(inputs)

def run(program_text, func):
	global all_linear,forcing_ok,stack,directed,solutions,path_constraints

	all_linear,forcing_ok = True,True
	solutions = {}
	path_constraints = {}
	program = parseAST(program_text)
	program.body = [node for node in program.body if type(node) is FunctionDef and node.name==func.func_name]
	func_args = func.func_code.co_varnames[:func.func_code.co_argcount]

	while True:
		stack = []
		
		inputs = random_inputs(func_args)
		first = inputs

		directed = True
	
		while directed:
			try:
				inputs = execute_program(program,func,inputs)
			except KeyboardInterrupt:
				raise
			except:
				from sys import exc_info
				from traceback import print_tb
				print >> sys.stderr, exc_info()
				print_tb(exc_info()[-1])
				if forcing_ok:
					print "Bug found"
					exit()
				else:
					forcing_ok = True
	
		if first:
			solutions[first] = get_solutions(path_constraints[first],first.keys())
			solutions[first] = filter_inputs(solutions[first],first.keys())

		if all_linear:
			break

	return solutions
