import unittest
from app.utils import *

class Utils(unittest.TestCase):

    club_names = ['fake']

    def testValidateMemberException(self):
        memberObj = {}
        with self.assertRaises(Exception) as exc:
            validateMember(memberObj, False, self.club_names)
        self.assertIsInstance(exc.exception, Exception)

    def testValidateMember(self):
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
            self.club_names
        )['success'], False)

