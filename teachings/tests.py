from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

from .models import TrainingClass
from people.models import MartialArtist
from styles.models import Style


class TrainingClassModelTests(TestCase):
    """Test cases for the TrainingClass model"""

    def setUp(self):
        self.style1 = Style.objects.create(title='Karate')
        self.style2 = Style.objects.create(title='Judo')
        self.instructor1 = MartialArtist.objects.create(
            first_name='Sensei',
            last_name='One'
        )
        self.instructor2 = MartialArtist.objects.create(
            first_name='Sensei',
            last_name='Two'
        )
        self.student1 = MartialArtist.objects.create(
            first_name='Student',
            last_name='One'
        )
        self.student2 = MartialArtist.objects.create(
            first_name='Student',
            last_name='Two'
        )

    def test_training_class_creation(self):
        """Test creating a training class with all fields"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 30, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time,
            notes='Beginner class'
        )
        training_class.instructors.add(self.instructor1, self.instructor2)
        training_class.students.add(self.student1, self.student2)
        training_class.focus.add(self.style1)
        
        self.assertEqual(training_class.start, start_time)
        self.assertEqual(training_class.end, end_time)
        self.assertEqual(training_class.instructors.count(), 2)
        self.assertEqual(training_class.students.count(), 2)
        self.assertEqual(training_class.focus.count(), 1)

    def test_training_class_creation_minimal_fields(self):
        """Test creating a training class with only required fields"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        self.assertEqual(training_class.start, start_time)
        self.assertEqual(training_class.end, end_time)
        self.assertEqual(training_class.instructors.count(), 0)
        self.assertEqual(training_class.students.count(), 0)

    def test_training_class_duration_in_mins(self):
        """Test duration_in_mins calculation"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 30, 0)  # 90 minutes later
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        self.assertEqual(training_class.duration_in_mins(), 90.0)

    def test_training_class_duration_one_hour(self):
        """Test duration_in_mins for one hour class"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)  # 60 minutes later
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        self.assertEqual(training_class.duration_in_mins(), 60.0)

    def test_training_class_duration_fractional_minutes(self):
        """Test duration_in_mins with fractional minutes"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 18, 45, 30)  # 45.5 minutes later
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        self.assertAlmostEqual(training_class.duration_in_mins(), 45.5, places=1)

    def test_training_class_many_to_many_instructors(self):
        """Test many-to-many relationship with instructors"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        training_class.instructors.add(self.instructor1, self.instructor2)
        
        self.assertEqual(training_class.instructors.count(), 2)
        self.assertIn(self.instructor1, training_class.instructors.all())
        self.assertIn(self.instructor2, training_class.instructors.all())

    def test_training_class_many_to_many_students(self):
        """Test many-to-many relationship with students"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        training_class.students.add(self.student1, self.student2)
        
        self.assertEqual(training_class.students.count(), 2)
        self.assertIn(self.student1, training_class.students.all())
        self.assertIn(self.student2, training_class.students.all())

    def test_training_class_many_to_many_focus(self):
        """Test many-to-many relationship with focus styles"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        training_class.focus.add(self.style1, self.style2)
        
        self.assertEqual(training_class.focus.count(), 2)
        self.assertIn(self.style1, training_class.focus.all())
        self.assertIn(self.style2, training_class.focus.all())

    def test_training_class_instructor_can_be_student(self):
        """Test that an instructor can also be a student"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time
        )
        training_class.instructors.add(self.instructor1)
        training_class.students.add(self.instructor1)  # Same person
        
        self.assertEqual(training_class.instructors.count(), 1)
        self.assertEqual(training_class.students.count(), 1)
        self.assertIn(self.instructor1, training_class.instructors.all())
        self.assertIn(self.instructor1, training_class.students.all())

    def test_training_class_validation_requires_start(self):
        """Test that training class requires start time"""
        training_class = TrainingClass(end=datetime(2024, 1, 15, 19, 0, 0))
        with self.assertRaises(ValidationError):
            training_class.full_clean()

    def test_training_class_validation_requires_end(self):
        """Test that training class requires end time"""
        training_class = TrainingClass(start=datetime(2024, 1, 15, 18, 0, 0))
        with self.assertRaises(ValidationError):
            training_class.full_clean()

    def test_training_class_verbose_name(self):
        """Test verbose name for TrainingClass"""
        self.assertEqual(TrainingClass._meta.verbose_name, 'Class')
        self.assertEqual(TrainingClass._meta.verbose_name_plural, 'Classes')

    def test_training_class_with_notes(self):
        """Test training class with notes"""
        start_time = datetime(2024, 1, 15, 18, 0, 0)
        end_time = datetime(2024, 1, 15, 19, 0, 0)
        
        training_class = TrainingClass.objects.create(
            start=start_time,
            end=end_time,
            notes='Focus on kata practice'
        )
        self.assertEqual(training_class.notes, 'Focus on kata practice')
