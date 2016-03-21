from django.test import TestCase
from flats.models import Flat, Person


class FlatModelTest(TestCase):

    def test_Meta(self):
        self.assertEqual(Flat._meta.verbose_name, ('квартира'))
        self.assertEqual(Flat._meta.verbose_name_plural, ('квартири'))


class PersonModelTest(TestCase):

    def test_Meta(self):
        self.assertEqual(Person._meta.verbose_name, ('особа'))
        self.assertEqual(Person._meta.verbose_name_plural, ('особи'))



