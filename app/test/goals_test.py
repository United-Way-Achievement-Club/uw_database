import unittest
from app.db_accessor import *
from goals_test_object import goal_valid, goal_invalid, create_goal

class Goal(unittest.TestCase):

	def setUp(self):
		addGoal(goal_valid)

	def testAddGoal(self):
		goal = getGoal(goal_valid['goal_name'])
		self.assertEqual(goal.goal_name, goal_valid['goal_name'])
		self.assertEqual(len(goal.steps), 3)
		self.assertEqual(len(goal.steps[0].proofs),3)

	def testEditGoalDeleteProof(self):
		edit_goal = goal_valid
		del edit_goal['steps'][0]['proofs'][0]
		editGoal(edit_goal)
		goal = getGoal(edit_goal['goal_name'])
		self.assertEqual(len(goal.steps[0].proofs), 2)

	def testEditGoalRenameStep(self):
		edit_goal = goal_valid
		edit_goal['steps'][1]['step_name'] = 'New Step 2'
		editGoal(edit_goal)
		goal = getGoal(edit_goal['goal_name'])
		self.assertEqual(goal.steps[1].step_name, 'New Step 2')

	def testIntegrityError(self):
		exc = addGoal(goal_valid)
		self.assertFalse(exc['success'])

	def testDeleteGoal(self):
		delete_goal = create_goal('Test Create Goal')
		addGoal(delete_goal)
		goal = getGoal(delete_goal['goal_name'])
		self.assertEqual(goal.goal_name, delete_goal['goal_name'])
		deleteGoal(delete_goal['goal_name'])
		goal = getGoal(delete_goal['goal_name'])
		self.assertEqual(goal, None)
		step = getStep(delete_goal['steps'][0]['step_name'], delete_goal['goal_name'])
		self.assertEqual(step, None)

	def tearDown(self):
		deleteGoal(goal_valid['goal_name'])




    