import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import Bug
from .views import DetailView

class BugModelTests(TestCase):
    def test_was_published_recently_with_future_bug(self):
        """
        was_published_recently() should return False for bugs whose
        report_date is in the future
        """

        time = timezone.now() + datetime.timedelta(days=2)
        future_bug = Bug(report_date=time)
        self.assertIs(future_bug.was_published_recently(), False)


    def test_field_types(self):
        """Verifying field types"""
        bug = Bug(description="Wrong Spelling", bug_type="Documentation", report_date=datetime.datetime.now(), status="In progress")
        self.assertIsInstance(bug.description, str)
        self.assertIsInstance(bug.bug_type, str)
        self.assertIsInstance(bug.report_date, datetime.datetime)
        self.assertIsInstance(bug.status, str)


    def test_long_description(self):
        description = "A"*300
        bug = Bug(description=description, bug_type="Documentation", report_date="2021-14-13", status="In Progress")
        self.assertRaises(ValidationError, bug.full_clean)

    def test_bug_filled_model(self):
        """All fields properly filled"""

        bug1 = Bug(description="This is a Sample Bug", 
                bug_type="UI",
                report_date=datetime.datetime.now(),
                status="Not Done"
            )
        assert bug1.description == "This is a Sample Bug"
        assert bug1.bug_type == "UI"
        assert isinstance(bug1.report_date, datetime.datetime)
        assert bug1.status == "Not Done"

    def test_bug_model_type(self):
        """supply an integer value to a CharField (like description)"""
        try:
            bug2 = Bug(description=12345, 
                    bug_type="UI",
                    report_date=datetime.datetime.now(),
                    status="Not Done"
                )
            bug2.full_clean() 
        except ValidationError as e:
            assert 'description' in e.message_dict



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
    def test_no_bugs(self):
        """ No bug registered the list should be empty """
        url = ("/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_bug_list'], [])

    def test_five_bugs(self):
        """Just five bug registered should display all the five bugs"""
        for i in range(1, 6):
            Bug.objects.create(description=f"Bug {i}", report_date=timezone.now())
        
        url = ("/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_bug_list']), 5)

    def test_more_than_five_bugs(self):
        """ More than five bug registered it should display on five bug as mentioned in the view"""
        for i in range(1, 7):
            Bug.objects.create(description=f"Bug {i}", report_date=timezone.now())
        
        url = ("/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_bug_list']), 5)

class DetailViewTestCase(TestCase):

    def test_invalid_bug_id(self):
        """ Invalid bug id check"""
        invalid_id = 1800
        url = 'detail/'+str(invalid_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RegistersBugViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = '/register-bug/' 
        
    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
    
    
    