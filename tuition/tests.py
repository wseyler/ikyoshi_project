from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from .models import PaymentPlan, TuitionPayment
from people.models import MartialArtist


class PaymentPlanModelTests(TestCase):
    """Test cases for the PaymentPlan model"""

    def test_payment_plan_creation(self):
        """Test creating a payment plan with all fields"""
        plan = PaymentPlan.objects.create(
            title='Monthly Plan',
            amount=Decimal('100.00'),
            frequency=PaymentPlan.MONTHLY_FREQUENCY,
            notes='Standard monthly payment'
        )
        self.assertEqual(plan.title, 'Monthly Plan')
        self.assertEqual(plan.amount, Decimal('100.00'))
        self.assertEqual(plan.frequency, PaymentPlan.MONTHLY_FREQUENCY)
        self.assertEqual(plan.notes, 'Standard monthly payment')

    def test_payment_plan_creation_minimal_fields(self):
        """Test creating a payment plan with only required fields"""
        plan = PaymentPlan.objects.create(
            title='Annual Plan',
            amount=Decimal('1000.00')
        )
        self.assertEqual(plan.title, 'Annual Plan')
        self.assertEqual(plan.amount, Decimal('1000.00'))
        self.assertEqual(plan.frequency, PaymentPlan.MONTHLY_FREQUENCY)  # Default

    def test_payment_plan_str_representation(self):
        """Test PaymentPlan string representation"""
        plan = PaymentPlan.objects.create(
            title='Monthly Plan',
            amount=Decimal('100.00')
        )
        self.assertEqual(str(plan), 'Monthly Plan')

    def test_payment_plan_default_frequency(self):
        """Test that frequency defaults to MONTHLY_FREQUENCY"""
        plan = PaymentPlan.objects.create(
            title='Plan',
            amount=Decimal('100.00')
        )
        self.assertEqual(plan.frequency, PaymentPlan.MONTHLY_FREQUENCY)

    def test_payment_plan_frequency_choices(self):
        """Test all frequency choices"""
        frequencies = [
            PaymentPlan.NONE_FREQUENCY,
            PaymentPlan.MONTHLY_FREQUENCY,
            PaymentPlan.BI_MONTHLY_FREQUENCY,
            PaymentPlan.QUARTERLY_FREQUENCY,
            PaymentPlan.SEMI_ANNUAL_FREQENCY,
            PaymentPlan.ANNUAL_FREQUENCY,
        ]
        
        for freq in frequencies:
            plan = PaymentPlan.objects.create(
                title=f'Plan {freq}',
                amount=Decimal('100.00'),
                frequency=freq
            )
            self.assertEqual(plan.frequency, freq)

    def test_payment_plan_validation_requires_title(self):
        """Test that payment plan requires title"""
        plan = PaymentPlan(amount=Decimal('100.00'))
        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_payment_plan_validation_requires_amount(self):
        """Test that payment plan requires amount"""
        plan = PaymentPlan(title='Plan')
        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_payment_plan_with_different_amounts(self):
        """Test payment plans with different amounts"""
        plan1 = PaymentPlan.objects.create(
            title='Basic Plan',
            amount=Decimal('50.00')
        )
        plan2 = PaymentPlan.objects.create(
            title='Premium Plan',
            amount=Decimal('150.00')
        )
        
        self.assertEqual(plan1.amount, Decimal('50.00'))
        self.assertEqual(plan2.amount, Decimal('150.00'))


class TuitionPaymentModelTests(TestCase):
    """Test cases for the TuitionPayment model"""

    def setUp(self):
        self.martial_artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.payment_plan = PaymentPlan.objects.create(
            title='Monthly Plan',
            amount=Decimal('100.00')
        )

    def test_tuition_payment_creation(self):
        """Test creating a tuition payment with all fields"""
        payment = TuitionPayment.objects.create(
            payment_plan=self.payment_plan,
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00'),
            notes='January payment'
        )
        self.assertEqual(payment.payment_plan, self.payment_plan)
        self.assertEqual(payment.payer, self.martial_artist)
        self.assertEqual(payment.date_paid, date(2024, 1, 15))
        self.assertEqual(payment.paid, Decimal('100.00'))
        self.assertEqual(payment.notes, 'January payment')

    def test_tuition_payment_creation_minimal_fields(self):
        """Test creating a tuition payment with only required fields"""
        payment = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        self.assertEqual(payment.payer, self.martial_artist)
        self.assertEqual(payment.date_paid, date(2024, 1, 15))
        self.assertEqual(payment.paid, Decimal('100.00'))
        self.assertIsNone(payment.payment_plan)

    def test_tuition_payment_str_representation(self):
        """Test TuitionPayment string representation"""
        payment = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        expected = '01/15/2024 - John Doe - $100.00'
        self.assertEqual(str(payment), expected)

    def test_tuition_payment_str_with_different_date(self):
        """Test TuitionPayment string representation with different date"""
        payment = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 12, 25),
            paid=Decimal('150.50')
        )
        expected = '12/25/2024 - John Doe - $150.50'
        self.assertEqual(str(payment), expected)

    def test_tuition_payment_validation_requires_payer(self):
        """Test that tuition payment requires payer"""
        payment = TuitionPayment(
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_tuition_payment_validation_requires_date_paid(self):
        """Test that tuition payment requires date_paid"""
        payment = TuitionPayment(
            payer=self.martial_artist,
            paid=Decimal('100.00')
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_tuition_payment_validation_requires_paid(self):
        """Test that tuition payment requires paid amount"""
        payment = TuitionPayment(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15)
        )
        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_tuition_payment_cascade_delete_martial_artist(self):
        """Test that payment is deleted when martial artist is deleted"""
        payment = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        self.martial_artist.delete()
        self.assertFalse(TuitionPayment.objects.filter(id=payment.id).exists())

    def test_tuition_payment_set_null_payment_plan_on_delete(self):
        """Test that payment_plan is set to None when plan is deleted"""
        payment = TuitionPayment.objects.create(
            payment_plan=self.payment_plan,
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        self.payment_plan.delete()
        payment.refresh_from_db()
        self.assertIsNone(payment.payment_plan)

    def test_tuition_payment_multiple_payments_per_artist(self):
        """Test that a martial artist can have multiple payments"""
        payment1 = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        payment2 = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 2, 15),
            paid=Decimal('100.00')
        )
        
        self.assertEqual(self.martial_artist.tuitionpayment_set.count(), 2)
        self.assertIn(payment1, self.martial_artist.tuitionpayment_set.all())
        self.assertIn(payment2, self.martial_artist.tuitionpayment_set.all())

    def test_tuition_payment_different_amounts(self):
        """Test payments with different amounts"""
        payment1 = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00')
        )
        payment2 = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 2, 15),
            paid=Decimal('150.50')
        )
        
        self.assertEqual(payment1.paid, Decimal('100.00'))
        self.assertEqual(payment2.paid, Decimal('150.50'))

    def test_tuition_payment_with_notes(self):
        """Test payment with notes"""
        payment = TuitionPayment.objects.create(
            payer=self.martial_artist,
            date_paid=date(2024, 1, 15),
            paid=Decimal('100.00'),
            notes='Partial payment'
        )
        self.assertEqual(payment.notes, 'Partial payment')
