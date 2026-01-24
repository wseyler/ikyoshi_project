from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date

from .models import RankType, Rank
from styles.models import Style
from people.models import MartialArtist


class RankTypeModelTests(TestCase):
    """Test cases for the RankType model"""

    def setUp(self):
        self.style = Style.objects.create(title='Karate')

    def test_rank_type_creation(self):
        """Test creating a rank type with all fields"""
        rank_type = RankType.objects.create(
            style=self.style,
            ordinal=1,
            title='White Belt',
            indicator='10th Kyu',
            time_in_grade=0,
            time_in_style=0,
            test_required=False,
            notes='Beginner rank'
        )
        self.assertEqual(rank_type.style, self.style)
        self.assertEqual(rank_type.ordinal, 1)
        self.assertEqual(rank_type.title, 'White Belt')
        self.assertEqual(rank_type.indicator, '10th Kyu')
        self.assertFalse(rank_type.test_required)

    def test_rank_type_creation_minimal_fields(self):
        """Test creating a rank type with only required fields"""
        rank_type = RankType.objects.create(
            style=self.style,
            title='White Belt'
        )
        self.assertEqual(rank_type.style, self.style)
        self.assertEqual(rank_type.title, 'White Belt')
        # ordinal defaults to 0, but if not provided Django may auto-assign
        self.assertIsNotNone(rank_type.ordinal)

    def test_rank_type_str_representation(self):
        """Test RankType string representation"""
        rank_type = RankType.objects.create(
            style=self.style,
            ordinal=1,
            title='White Belt',
            indicator='10th Kyu'
        )
        expected = f'{self.style.title}, White Belt (10th Kyu)'
        self.assertEqual(str(rank_type), expected)

    def test_rank_type_default_ordinal(self):
        """Test that ordinal defaults to 0"""
        rank_type = RankType.objects.create(
            style=self.style,
            title='White Belt'
        )
        self.assertEqual(rank_type.ordinal, 0)

    def test_rank_type_default_test_required(self):
        """Test that test_required defaults to False"""
        rank_type = RankType.objects.create(
            style=self.style,
            title='White Belt'
        )
        self.assertFalse(rank_type.test_required)

    def test_rank_type_ordering(self):
        """Test that rank types are ordered by ordinal"""
        rank_type1 = RankType.objects.create(
            style=self.style,
            ordinal=3,
            title='Brown Belt'
        )
        rank_type2 = RankType.objects.create(
            style=self.style,
            ordinal=1,
            title='White Belt'
        )
        rank_type3 = RankType.objects.create(
            style=self.style,
            ordinal=2,
            title='Yellow Belt'
        )
        
        rank_types = list(RankType.objects.all())
        self.assertEqual(rank_types[0], rank_type2)  # ordinal 1
        self.assertEqual(rank_types[1], rank_type3)  # ordinal 2
        self.assertEqual(rank_types[2], rank_type1)  # ordinal 3

    def test_rank_type_validation_requires_style(self):
        """Test that rank type requires style"""
        rank_type = RankType(ordinal=1, title='White Belt')
        with self.assertRaises(ValidationError):
            rank_type.full_clean()

    def test_rank_type_validation_requires_title(self):
        """Test that rank type requires title"""
        rank_type = RankType(style=self.style, ordinal=1)
        with self.assertRaises(ValidationError):
            rank_type.full_clean()

    def test_rank_type_cascade_delete_style(self):
        """Test that rank type is deleted when style is deleted"""
        rank_type = RankType.objects.create(
            style=self.style,
            ordinal=1,
            title='White Belt'
        )
        self.style.delete()
        self.assertFalse(RankType.objects.filter(id=rank_type.id).exists())


class RankModelTests(TestCase):
    """Test cases for the Rank model"""

    def setUp(self):
        self.style = Style.objects.create(title='Karate')
        self.martial_artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.rank_type = RankType.objects.create(
            style=self.style,
            ordinal=1,
            title='White Belt',
            indicator='10th Kyu'
        )

    def test_rank_creation(self):
        """Test creating a rank with all fields"""
        rank = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            test_date=date(2020, 1, 15),
            award_date=date(2020, 1, 20),
            tested=True,
            notes='Excellent performance'
        )
        self.assertEqual(rank.martial_artist, self.martial_artist)
        self.assertEqual(rank.rank_type, self.rank_type)
        self.assertEqual(rank.test_date, date(2020, 1, 15))
        self.assertEqual(rank.award_date, date(2020, 1, 20))
        self.assertTrue(rank.tested)

    def test_rank_creation_minimal_fields(self):
        """Test creating a rank with only required fields"""
        rank = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            award_date=date(2020, 1, 20)
        )
        self.assertEqual(rank.martial_artist, self.martial_artist)
        self.assertEqual(rank.rank_type, self.rank_type)
        self.assertIsNone(rank.test_date)
        self.assertTrue(rank.tested)  # Default is True

    def test_rank_str_representation(self):
        """Test Rank string representation"""
        rank = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            award_date=date(2020, 1, 20)
        )
        expected = f'{self.martial_artist}: {self.rank_type} -- 2020-01-20'
        self.assertEqual(str(rank), expected)

    def test_rank_default_tested(self):
        """Test that tested defaults to True"""
        rank = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            award_date=date(2020, 1, 20)
        )
        self.assertTrue(rank.tested)

    def test_rank_validation_requires_martial_artist(self):
        """Test that rank requires martial_artist"""
        rank = Rank(rank_type=self.rank_type, award_date=date(2020, 1, 20))
        with self.assertRaises(ValidationError):
            rank.full_clean()

    def test_rank_validation_requires_rank_type(self):
        """Test that rank requires rank_type"""
        rank = Rank(martial_artist=self.martial_artist, award_date=date(2020, 1, 20))
        with self.assertRaises(ValidationError):
            rank.full_clean()

    def test_rank_validation_requires_award_date(self):
        """Test that rank requires award_date"""
        rank = Rank(martial_artist=self.martial_artist, rank_type=self.rank_type)
        with self.assertRaises(ValidationError):
            rank.full_clean()

    def test_rank_cascade_delete_martial_artist(self):
        """Test that rank is deleted when martial artist is deleted"""
        rank = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            award_date=date(2020, 1, 20)
        )
        self.martial_artist.delete()
        self.assertFalse(Rank.objects.filter(id=rank.id).exists())

    def test_rank_protect_delete_rank_type(self):
        """Test that rank type cannot be deleted if rank exists (PROTECT)"""
        rank = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            award_date=date(2020, 1, 20)
        )
        with self.assertRaises(Exception):  # ProtectedError
            self.rank_type.delete()
        
        # Verify rank type still exists
        self.assertTrue(RankType.objects.filter(id=self.rank_type.id).exists())

    def test_rank_multiple_ranks_per_artist(self):
        """Test that a martial artist can have multiple ranks"""
        rank_type2 = RankType.objects.create(
            style=self.style,
            ordinal=2,
            title='Yellow Belt',
            indicator='9th Kyu'
        )
        rank1 = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=self.rank_type,
            award_date=date(2020, 1, 20)
        )
        rank2 = Rank.objects.create(
            martial_artist=self.martial_artist,
            rank_type=rank_type2,
            award_date=date(2020, 6, 20)
        )
        
        self.assertEqual(self.martial_artist.rank_set.count(), 2)
        self.assertIn(rank1, self.martial_artist.rank_set.all())
        self.assertIn(rank2, self.martial_artist.rank_set.all())
