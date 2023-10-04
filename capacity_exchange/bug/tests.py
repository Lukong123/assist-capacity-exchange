import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Bug

class BugModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for bugs whose
        report_date is in the future
        """

        time = timezone.now() + datetime.timedelta(days=2)
        future_bug = Bug(report_date=time)
        self.assertIs(future_bug.was_published_recently(), False)


    def test_field_types(self):
        bug = Bug(description="Wrong Spelling", bug_type="Documentation", report_date=datetime.datetime.now(), status="In progress")
        self.assertIsInstance(bug.description, str)
        self.assertIsInstance(bug.bug_type, str)
        self.assertIsInstance(bug.report_date, datetime.datetime)
        self.assertIsInstance(bug.status, str)
    
    def test_valid_input(self):
        bug = Bug(description="Valid Test", bug_type="bug", report_date=datetime.datetime.now(), status="Not Done")
        self.assertEqual(str(bug), "bug")
    
    def test_empty_description(self):
        bug = Bug(description="", bug_type="Documentation", report_date=datetime.datetime.now(), status="In Progress")
        with self.assertRaises(ValidationError) as context:
            errors = bug.full_clean()
        self.assertIn('description', errors)

    def test_invalid_report_date(self):
        bug = Bug(description="Know Explanation", bug_type="Documentation", report_date="2021-14-13", status="In Progress")
        with self.assertRaises(ValidationError) as context:
            bug.full_clean()
        self.assertTrue("report_date" in context.exception.message_dict)

    def test_long_description(self):
        description = "A"*300
        bug = Bug(description=description, bug_type="Documentation", report_date="2021-14-13", status="In Progress")
        self.assertRaises(ValidationError, bug.full_clean)
        # do for future date