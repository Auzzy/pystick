from constraint import *

MAX_VAL = 10

def _constraint_from_strings(vars, constraint):
	var_str = str(vars)[1:-1].replace('\'','')
	func_str = "lambda {0}: {1}".format(var_str,str(constraint))
	return eval(func_str)

def get_solutions(path_constraints, scope_vars):
	problem = Problem()
	problem.addVariables(scope_vars,range(-MAX_VAL,MAX_VAL+1))

	for constraint in path_constraints:
		constraint_func = _constraint_from_strings(scope_vars,constraint)
		problem.addConstraint(constraint_func,scope_vars)
	
	return problem.getSolutions()
