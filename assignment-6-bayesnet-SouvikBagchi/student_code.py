
from copy import deepcopy
import pdb

def ask(var, value, evidence, bn):
	#create a new dictionary with the var and the value
	new_evidence_1 = deepcopy(evidence)
	new_evidence_1[var] = value

	new_evidence_2 = deepcopy(evidence)
	new_evidence_2[var] = neg_value(value)

	# pdb.set_trace()
	#pass in the list of nodes
	list_of_var = bn.variables
	#pdb.set_trace()
	prob1 = helper_probability(new_evidence_1, list_of_var)
	prob2 = helper_probability(new_evidence_2, list_of_var)

	return prob1/(prob1+prob2)
def neg_value(value):
	if value == True:
		return False
	else:
		return True	
				
def helper_probability(evidence, list_of_var):

	#base condition
	if(len(list_of_var)==0):
		return 1.0

	node = list_of_var[0]
	#first condition that the node is in the evidence
	if (node.name in evidence):
		#make new copy of evidence
		prob = node.probability(evidence[node.name],evidence)*helper_probability(evidence, list_of_var[1:])
		return prob

	#else if the node is not in evidence
	else:

		#make two copies of evidence
		new_evidence_1 = dict(evidence)
		new_evidence_1[node.name] = True

		new_evidence_2 = dict(evidence)
		new_evidence_2[node.name] = False
		
		prob_1 = node.probability(True, evidence)*helper_probability(new_evidence_1, list_of_var[1:])
		prob_2 = node.probability(False, evidence)*helper_probability(new_evidence_2, list_of_var[1:])

		return (prob_1+prob_2)


