from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Style


class StyleModelTests(TestCase):
    """Test cases for the Style model"""

    def test_style_creation(self):
        """Test creating a style with all fields"""
        style = Style.objects.create(
            title='Karate',
            originator='Gichin Funakoshi',
            notes='Japanese martial art'
        )
        self.assertEqual(style.title, 'Karate')
        self.assertEqual(style.originator, 'Gichin Funakoshi')
        self.assertEqual(style.notes, 'Japanese martial art')

    def test_style_creation_minimal_fields(self):
        """Test creating a style with only required fields"""
        style = Style.objects.create(title='Judo')
        self.assertEqual(style.title, 'Judo')
        self.assertIsNone(style.originator)
        self.assertIsNone(style.notes)

    def test_style_str_representation(self):
        """Test Style string representation"""
        style = Style.objects.create(title='Karate')
        self.assertEqual(str(style), 'Karate')

    def test_style_validation_requires_title(self):
        """Test that style requires title"""
        style = Style()
        with self.assertRaises(ValidationError):
            style.full_clean()

    def test_style_title_max_length(self):
        """Test that style title respects max_length"""
        style = Style.objects.create(title='A' * 30)  # Max length
        self.assertEqual(len(style.title), 30)

    def test_style_unique_titles_allowed(self):
        """Test that multiple styles with same title are allowed"""
        style1 = Style.objects.create(title='Karate')
        style2 = Style.objects.create(title='Karate')
        self.assertEqual(Style.objects.filter(title='Karate').count(), 2)

    def test_style_with_originator(self):
        """Test style with originator field"""
        style = Style.objects.create(
            title='Aikido',
            originator='Morihei Ueshiba'
        )
        self.assertEqual(style.originator, 'Morihei Ueshiba')

    def test_style_with_notes(self):
        """Test style with notes field"""
        style = Style.objects.create(
            title='Taekwondo',
            notes='Korean martial art focusing on kicking techniques'
        )
        self.assertIsNotNone(style.notes)
        self.assertIn('Korean', style.notes)
