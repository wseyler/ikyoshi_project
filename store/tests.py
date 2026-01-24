from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal

from .models import Item, Invoice, LineItem
from people.models import MartialArtist


class ItemModelTests(TestCase):
    """Test cases for the Item model"""

    def test_item_creation(self):
        """Test creating an item with all fields"""
        item = Item.objects.create(
            name='Gi',
            make='Adidas',
            sku='GI-001',
            size='M',
            color='White',
            wholesale_price=Decimal('50.00'),
            retail_price=Decimal('75.00'),
            quantity_on_hand=10,
            notes='Standard karate gi'
        )
        self.assertEqual(item.name, 'Gi')
        self.assertEqual(item.make, 'Adidas')
        self.assertEqual(item.sku, 'GI-001')
        self.assertEqual(item.size, 'M')
        self.assertEqual(item.color, 'White')
        self.assertEqual(item.wholesale_price, Decimal('50.00'))
        self.assertEqual(item.retail_price, Decimal('75.00'))
        self.assertEqual(item.quantity_on_hand, 10)

    def test_item_creation_minimal_fields(self):
        """Test creating an item with only required fields"""
        item = Item.objects.create(
            name='Belt',
            retail_price=Decimal('15.00')
        )
        self.assertEqual(item.name, 'Belt')
        self.assertEqual(item.retail_price, Decimal('15.00'))
        self.assertEqual(item.quantity_on_hand, 0)  # Default

    def test_item_str_representation(self):
        """Test Item string representation"""
        item = Item.objects.create(
            name='Gi',
            retail_price=Decimal('75.00')
        )
        self.assertEqual(str(item), 'Gi')

    def test_item_default_quantity_on_hand(self):
        """Test that quantity_on_hand defaults to 0"""
        item = Item.objects.create(
            name='Belt',
            retail_price=Decimal('15.00')
        )
        self.assertEqual(item.quantity_on_hand, 0)

    def test_item_validation_requires_name(self):
        """Test that item requires name"""
        item = Item(retail_price=Decimal('15.00'))
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_item_validation_requires_retail_price(self):
        """Test that item requires retail_price"""
        item = Item(name='Belt')
        with self.assertRaises(ValidationError):
            item.full_clean()


class InvoiceModelTests(TestCase):
    """Test cases for the Invoice model"""

    def setUp(self):
        self.martial_artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )

    def test_invoice_creation(self):
        """Test creating an invoice"""
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist,
            notes='First purchase'
        )
        self.assertEqual(invoice.purchaser, self.martial_artist)
        self.assertIsNotNone(invoice.date_ordered)
        self.assertIsNone(invoice.date_completed)

    def test_invoice_str_representation(self):
        """Test Invoice string representation"""
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        self.assertEqual(str(invoice), str(invoice.id))

    def test_invoice_auto_date_ordered(self):
        """Test that date_ordered is automatically set"""
        from datetime import date
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        self.assertEqual(invoice.date_ordered, date.today())

    def test_invoice_validation_requires_purchaser(self):
        """Test that invoice requires purchaser"""
        invoice = Invoice()
        with self.assertRaises(ValidationError):
            invoice.full_clean()

    def test_invoice_cascade_delete_martial_artist(self):
        """Test that invoice is deleted when martial artist is deleted"""
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        self.martial_artist.delete()
        self.assertFalse(Invoice.objects.filter(id=invoice.id).exists())

    def test_invoice_total_no_line_items(self):
        """Test invoice_total with no line items"""
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        self.assertEqual(invoice.invoice_total(), 0)

    def test_invoice_total_with_line_items(self):
        """Test invoice_total calculation with line items"""
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        item1 = Item.objects.create(
            name='Gi',
            retail_price=Decimal('75.00')
        )
        item2 = Item.objects.create(
            name='Belt',
            retail_price=Decimal('15.00')
        )
        LineItem.objects.create(
            invoice=invoice,
            item=item1,
            quantity=2
        )
        LineItem.objects.create(
            invoice=invoice,
            item=item2,
            quantity=1
        )
        
        expected_total = Decimal('75.00') * 2 + Decimal('15.00') * 1
        self.assertEqual(invoice.invoice_total(), expected_total)

    def test_invoice_total_multiple_items_same_product(self):
        """Test invoice_total with multiple quantities of same item"""
        invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        item = Item.objects.create(
            name='Gi',
            retail_price=Decimal('75.00')
        )
        LineItem.objects.create(
            invoice=invoice,
            item=item,
            quantity=3
        )
        
        expected_total = Decimal('75.00') * 3
        self.assertEqual(invoice.invoice_total(), expected_total)


class LineItemModelTests(TestCase):
    """Test cases for the LineItem model"""

    def setUp(self):
        self.martial_artist = MartialArtist.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.invoice = Invoice.objects.create(
            purchaser=self.martial_artist
        )
        self.item = Item.objects.create(
            name='Gi',
            retail_price=Decimal('75.00')
        )

    def test_line_item_creation(self):
        """Test creating a line item"""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            item=self.item,
            quantity=2
        )
        self.assertEqual(line_item.invoice, self.invoice)
        self.assertEqual(line_item.item, self.item)
        self.assertEqual(line_item.quantity, 2)

    def test_line_item_creation_default_quantity(self):
        """Test creating a line item with default quantity"""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            item=self.item
        )
        self.assertEqual(line_item.quantity, 1)  # Default

    def test_line_item_default_quantity(self):
        """Test that quantity defaults to 1"""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            item=self.item
        )
        self.assertEqual(line_item.quantity, 1)

    def test_line_item_validation_requires_invoice(self):
        """Test that line item requires invoice"""
        line_item = LineItem(item=self.item, quantity=1)
        with self.assertRaises(ValidationError):
            line_item.full_clean()

    def test_line_item_validation_requires_item(self):
        """Test that line item requires item"""
        line_item = LineItem(invoice=self.invoice, quantity=1)
        with self.assertRaises(ValidationError):
            line_item.full_clean()

    def test_line_item_cascade_delete_invoice(self):
        """Test that line item is deleted when invoice is deleted"""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            item=self.item,
            quantity=2
        )
        self.invoice.delete()
        self.assertFalse(LineItem.objects.filter(id=line_item.id).exists())

    def test_line_item_cascade_delete_item(self):
        """Test that line item is deleted when item is deleted"""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            item=self.item,
            quantity=2
        )
        self.item.delete()
        self.assertFalse(LineItem.objects.filter(id=line_item.id).exists())

    def test_line_item_multiple_items_per_invoice(self):
        """Test that an invoice can have multiple line items"""
        item2 = Item.objects.create(
            name='Belt',
            retail_price=Decimal('15.00')
        )
        line_item1 = LineItem.objects.create(
            invoice=self.invoice,
            item=self.item,
            quantity=1
        )
        line_item2 = LineItem.objects.create(
            invoice=self.invoice,
            item=item2,
            quantity=2
        )
        
        self.assertEqual(self.invoice.lineitem_set.count(), 2)
        self.assertIn(line_item1, self.invoice.lineitem_set.all())
        self.assertIn(line_item2, self.invoice.lineitem_set.all())
