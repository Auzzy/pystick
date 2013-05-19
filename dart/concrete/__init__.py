from concrete import eval as eval_concretely

def eval(program, func, inputs={}):
	return eval_concretely(program,func,inputs)
