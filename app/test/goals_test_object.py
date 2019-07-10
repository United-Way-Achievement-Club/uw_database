import unittest
from app import db, models

def create_goal(goal_name):
	goal = {
		'goal_name':goal_name,
		'goal_category':'Education',
		'num_of_steps':3,
		'steps':[create_step(x) for x in range(1,4)]
	}
	return goal

def create_step(step_num):
	step_name = 'Step ' + str(step_num)
	step = {
		'step_name':step_name,
		'proofs':[create_proof(x) for x in range(1,4)]
	}
	return step

def create_proof(proof_num):
	proof = {
		'proof_document':'Proof ' + str(proof_num),
		'proof_description': 'No description'
	}
	return proof

goal_valid = create_goal('Test Goal')
goal_invalid = {}



