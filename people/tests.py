from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Sponsor

class SponsorModelTests(TestCase):

    def test_for_successful_save_of_sponsor(self):
        test_sponsor = Sponsor(first_name='John', last_name='Doe')

        try:
            test_sponsor.full_clean()
        except ValidationError as e:
            self.assertTrue('email' in e.message_dict)

        test_sponsor.email = 'someone@nowhere.com'
        test_sponsor.save()
        self.assertTrue(test_sponsor.id > -1)


    def test_for_unsuccessful_save_of_sponsor(self):
        test_sponsor = Sponsor(first_name='John')
        self.assertIs(test_sponsor.id, None)
        
        try:
            test_sponsor.full_clean()
        except ValidationError as e:
            self.assertTrue('last_name' in e.message_dict)
