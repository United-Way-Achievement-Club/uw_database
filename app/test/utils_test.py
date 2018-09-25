import unittest
from app.utils import *
from test_objects import club_names, valid_member

class Utils(unittest.TestCase):

    def testValidateMemberException(self):
        memberObj = {}
        with self.assertRaises(Exception) as exc:
            validateMember(memberObj, False, club_names)
        self.assertIsInstance(exc.exception, Exception)

    def testValidateMemberInvalid(self):
        memberObj = {
            'general':[],
            'enrollment_form':[],
            'demographic_data':[],
            'self_sufficiency_matrix':[],
            'self_efficacy_quiz':[]
        }
        self.assertEqual(validateMember(
            memberObj,
            False,
            club_names
        )['success'], False)

    def testValidateMemberValid(self):
        self.assertEqual(validateMember(
            valid_member,
            False,
            club_names
        )['success'], True)

