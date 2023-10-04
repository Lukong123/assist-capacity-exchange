import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Bug
from .views import DetailView

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


# Creating Testcases For View

def create_bug(description, days):
    """
    Create a bug with the given `description` and published the
    given number of `days` offset to now which will return negative for bugs reported
    in the past and positive for bugs that are yet to be reported).
    """

    time = timezone.now() + datetime.timedelta(days=days)
    return Bug.objects.create(description=description, report_date=time)

class BugIndexViewTests(TestCase):

    def test_past_test(self):
        """
        Bugs  with a report_date in the past are displayed on the index page
        """
        bug = create_bug(description="Past bug.", days=-25)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerySetEqual(
            response.context["latest_bug_list"],
            [bug],
        )

    def test_two_past_bug(self):
        """
        The bug index page may display multiple bugs
        """
        bug_1 = create_bug(description="bug 1", days=-4)
        bug_2 = create_bug(description="bug 2", days = 6)
        response = self.client.get(reverse("bug:index"))
        self.assertQuerysetEqual(
            response.context["latest_bug_list"],
            [bug_1, bug_2]
        )
       
    def test_no_bugs(self):
        """ No bug registered the list should be empty """
        url = reverse('bug:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_bug_list'], [])

    def test_five_bugs(self):
        """Just five bug registered should display all the five bugs"""
        for i in range(1, 6):
            Bug.objects.create(description=f"Bug {i}", report_date=timezone.now())
        
        url = reverse('bug:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_bug_list']), 5)

    def test_more_than_five_bugs(self):
        """ More than five bug registered it should display on five bug as mentioned in the view"""
        for i in range(1, 7):
            Bug.objects.create(description=f"Bug {i}", report_date=timezone.now())
        
        url = reverse('bug:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_bug_list']), 5)

class DetailViewTestCase(TestCase):
    
    def test_bug_detail(self):
        """ Bug details verifying all fields"""
        bug = Bug.objects.create(
            description = "Test bug",
            bug_type = "Bug",
            status = "In Progress",
            report_date = datetime.datetime

        )
        url = reverse('bug:detail', args=[bug.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], bug)

        self.assertContains(response, bug.description)
        self.assertContains(response, bug.bug_type)
        self.assertContains(response, bug.status)
        self.assertContains(response, bug.report_date)

    def test_invalid_bug_id(self):
        """ Invalid bug id check"""
        invalid_id = 1800
        url = reverse('bug:detail', args=[invalid_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class RegisterBugViewTestCase(TestCase):
    def test_register_bug(self):
        """register bug check"""
        description = "Test Bug"
        url = reverse('bug:bug:register_bug')
        response = self.client.post(url, {'description': description})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('bug:bug:index'))

        bug = Bug.objects.get(description=description)
        self.assertEqual(bug.description, description)
        self.assertEqual(bug.report_date.date(), timezone.now().date())
