from symbolic import eval as eval_symbolically, Variable as Var

def eval(node, env, symbolic):
	return eval_symbolically(node,env,symbolic)

Variable = Var
