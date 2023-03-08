from django.test import TestCase
from unittest.mock import patch

from .views import calculate_cpa

# Create your tests here.


class TestFunctions(TestCase):

    
    def test_calculate_cpa(self):
        self.assertEquals(calculate_cpa(6,2), 3)

    def test_calculate_cpa_divide_by_zero(self):
        self.assertEquals(calculate_cpa(6,0), 0)
