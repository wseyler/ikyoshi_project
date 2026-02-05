from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from datetime import date

from .models import Person, Sponsor, MartialArtist
from .views import index
from styles.models import Style
from tuition.models import PaymentPlan


class PersonModelTests(TestCase):
    """Test cases for the abstract Person model (tested through Sponsor and MartialArtist)"""

    def test_person_abstract(self):
        """Test that Person is an abstract model"""
        self.assertTrue(Person._meta.abstract)


class SponsorModelTests(TestCase):
    """Test cases for the Sponsor model"""

    def test_sponsor_creation(self):
        """Test creating a sponsor with all fields"""
        sponsor = Sponsor.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            telephone='555-1234',
            street='123 Main St',
            city='Springfield',
            state='IL',
            zip='62701',
            isParent=True
        )
        self.assertEqual(sponsor.first_name, 'John')
        self.assertEqual(sponsor.last_name, 'Doe')
        self.assertEqual(sponsor.email, 'john@example.com')
        self.assertTrue(sponsor.isParent)

    def test_sponsor_creation_minimal_fields(self):
        """Test creating a sponsor with only required fields"""
        sponsor = Sponsor.objects.create(
            first_name='Jane',
            last_name='Smith'
        )
        self.assertEqual(sponsor.first_name, 'Jane')
        self.assertEqual(sponsor.last_name, 'Smith')
        self.assertIsNone(sponsor.email)
        self.assertIsNone(sponsor.telephone)

    def test_sponsor_str_representation(self):
        """Test Sponsor string representation"""
        sponsor = Sponsor.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(str(sponsor), 'John Doe')

    def test_sponsor_str_with_middle_name(self):
        """Test Sponsor string representation with middle name"""
        sponsor = Sponsor.objects.create(
            first_name='John',
            middle_name='Michael',
            last_name='Doe'
        )
        self.assertEqual(str(sponsor), 'John M. Doe')

    def test_sponsor_str_with_empty_middle_name(self):
        """Test Sponsor string representation with empty middle name"""
        sponsor = Sponsor.objects.create(
            first_name='John',
            middle_name='',
            last_name='Doe'
        )
        self.assertEqual(str(sponsor), 'John Doe')

    def test_sponsor_default_isParent(self):
        """Test that isParent defaults to True"""
        sponsor = Sponsor.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.assertTrue(sponsor.isParent)

    def test_sponsor_validation_requires_first_name(self):
        """Test that sponsor requires first_name"""
        sponsor = Sponsor(last_name='Doe')
        with self.assertRaises(ValidationError):
            sponsor.full_clean()

    def test_sponsor_validation_requires_last_name(self):
        """Test that sponsor requires last_name"""
        sponsor = Sponsor(first_name='John')
        with self.assertRaises(ValidationError):
            sponsor.full_clean()

    def test_sponsor_save_successful(self):
        """Test successful save of sponsor"""
        sponsor = Sponsor(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        sponsor.full_clean()
        sponsor.save()
        self.assertIsNotNone(sponsor.id)
        self.assertTrue(sponsor.id > 0)

    def test_sponsor_ordering(self):
        """Test that sponsors are ordered by last_name, first_name"""
        sponsor1 = Sponsor.objects.create(first_name='John', last_name='Doe')
        sponsor2 = Sponsor.objects.create(first_name='Jane', last_name='Adams')
        sponsor3 = Sponsor.objects.create(first_name='Bob', last_name='Doe')
        
        sponsors = list(Sponsor.objects.all())
        self.assertEqual(sponsors[0], sponsor2)  # Adams first
        self.assertEqual(sponsors[1], sponsor3)  # Doe, Bob
        self.assertEqual(sponsors[2], sponsor1)  # Doe, John


class MartialArtistModelTests(TestCase):
    """Test cases for the MartialArtist model"""

    def setUp(self):
        self.sponsor = Sponsor.objects.create(
            first_name='Parent',
            last_name='Sponsor',
            email='parent@example.com'
        )
        self.style1 = Style.objects.create(title='Karate')
        self.style2 = Style.objects.create(title='Judo')
        self.payment_plan = PaymentPlan.objects.create(
            title='Monthly Plan',
            amount=100.00
        )

    def test_martial_artist_creation(self):
        """Test creating a martial artist with all fields"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            birthday=date(2000, 1, 1),
            enrollment_date=date(2020, 1, 1),
            sponsor=self.sponsor,
            active=True,
            isFemale=False,
            payment_plan=self.payment_plan
        )
        artist.styles.add(self.style1, self.style2)
        
        self.assertEqual(artist.first_name, 'John')
        self.assertEqual(artist.last_name, 'Doe')
        self.assertEqual(artist.sponsor, self.sponsor)
        self.assertEqual(artist.payment_plan, self.payment_plan)
        self.assertTrue(artist.active)
        self.assertFalse(artist.isFemale)
        self.assertEqual(artist.styles.count(), 2)

    def test_martial_artist_creation_minimal_fields(self):
        """Test creating a martial artist with only required fields"""
        artist = MartialArtist.objects.create(
            first_name='Jane',
            last_name='Smith'
        )
        self.assertEqual(artist.first_name, 'Jane')
        self.assertEqual(artist.last_name, 'Smith')
        self.assertIsNone(artist.sponsor)
        self.assertIsNone(artist.payment_plan)
        self.assertTrue(artist.active)  # Default is True

    def test_martial_artist_str_representation(self):
        """Test MartialArtist string representation"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(str(artist), 'John Doe')

    def test_martial_artist_str_with_middle_name(self):
        """Test MartialArtist string representation with middle name"""
        artist = MartialArtist.objects.create(
            first_name='John',
            middle_name='Michael',
            last_name='Doe'
        )
        self.assertEqual(str(artist), 'John M. Doe')

    def test_martial_artist_default_active(self):
        """Test that active defaults to True"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.assertTrue(artist.active)

    def test_martial_artist_default_isFemale(self):
        """Test that isFemale defaults to False"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.assertFalse(artist.isFemale)

    def test_martial_artist_many_to_many_styles(self):
        """Test many-to-many relationship with styles"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        artist.styles.add(self.style1, self.style2)
        
        self.assertEqual(artist.styles.count(), 2)
        self.assertIn(self.style1, artist.styles.all())
        self.assertIn(self.style2, artist.styles.all())

    def test_martial_artist_foreign_key_sponsor(self):
        """Test foreign key relationship with sponsor"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe',
            sponsor=self.sponsor
        )
        self.assertEqual(artist.sponsor, self.sponsor)

    def test_martial_artist_sponsor_set_null_on_delete(self):
        """Test that sponsor is set to None when sponsor is deleted"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe',
            sponsor=self.sponsor
        )
        self.sponsor.delete()
        artist.refresh_from_db()
        self.assertIsNone(artist.sponsor)

    def test_martial_artist_foreign_key_payment_plan(self):
        """Test foreign key relationship with payment plan"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe',
            payment_plan=self.payment_plan
        )
        self.assertEqual(artist.payment_plan, self.payment_plan)

    def test_martial_artist_payment_plan_set_null_on_delete(self):
        """Test that payment_plan is set to None when plan is deleted"""
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe',
            payment_plan=self.payment_plan
        )
        self.payment_plan.delete()
        artist.refresh_from_db()
        self.assertIsNone(artist.payment_plan)

    def test_martial_artist_image_upload(self):
        """Test image field can be set"""
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe',
            image=image
        )
        self.assertIsNotNone(artist.image)

    def test_martial_artist_validation_requires_first_name(self):
        """Test that martial artist requires first_name"""
        artist = MartialArtist(last_name='Doe')
        with self.assertRaises(ValidationError):
            artist.full_clean()

    def test_martial_artist_validation_requires_last_name(self):
        """Test that martial artist requires last_name"""
        artist = MartialArtist(first_name='John')
        with self.assertRaises(ValidationError):
            artist.full_clean()

    def test_martial_artist_ordering(self):
        """Test that martial artists are ordered by last_name, first_name"""
        artist1 = MartialArtist.objects.create(first_name='John', last_name='Doe')
        artist2 = MartialArtist.objects.create(first_name='Jane', last_name='Adams')
        artist3 = MartialArtist.objects.create(first_name='Bob', last_name='Doe')
        
        artists = list(MartialArtist.objects.all())
        self.assertEqual(artists[0], artist2)  # Adams first
        self.assertEqual(artists[1], artist3)  # Doe, Bob
        self.assertEqual(artists[2], artist1)  # Doe, John


class PeopleViewsTests(TestCase):
    """Test cases for people views"""

    def setUp(self):
        self.client = Client()

    def test_index_requires_login(self):
        """People index redirects to login when not authenticated."""
        response = self.client.get('/people/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_index_shows_message_when_no_profile(self):
        """Authenticated user without a linked martial artist sees a message."""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='jane', password='testpass123')
        self.client.login(username='jane', password='testpass123')
        response = self.client.get('/people/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('No martial artist profile', response.content.decode('utf-8'))

    def test_index_shows_own_profile_when_linked(self):
        """Authenticated user with linked martial artist sees their profile."""
        from django.contrib.auth.models import User
        from .models import MartialArtist
        user = User.objects.create_user(username='jane', password='testpass123')
        ma = MartialArtist.objects.create(
            first_name='Jane', last_name='Doe', user=user
        )
        self.client.login(username='jane', password='testpass123')
        response = self.client.get('/people/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Jane', response.content.decode('utf-8'))
        self.assertIn('Doe', response.content.decode('utf-8'))
