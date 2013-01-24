#!/usr/bin/env python

"""Provides test cases for pyavrophonetic.avro.utils.validate

-------------------------------------------------------------------------------

Copyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.

This file is part of pyAvroPhonetic.

pyAvroPhonetic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyAvroPhonetic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyAvroPhonetic.  If not, see <http://www.gnu.org/licenses/>.

"""

# Imports
import unittest
from pyavrophonetic.utils import validate


class TestUtilsValidate(unittest.TestCase):
    """Tests validation methods for pyavrophonetic.utils.validate"""

    def setUp(self):
        """Set up test environment"""
        self.vowels = 'aeiou'
        self.consonants = 'bcdfghjklmnpqrstvwxyz'
        self.numbers = '0123456789'

    def test_is_consonant(self):
        """Test that consonants are correctly identified"""
        # Test all defined consonants. Should be True
        for i in self.consonants + self.consonants.upper():
            self.assertTrue(validate.is_consonant(i))
        # Test all defined consonants to be vowels or numbers. Should
        # be False
        for i in self.vowels + self.numbers:
            self.assertFalse(validate.is_consonant(i))

    def test_is_number(self):
        """Test that numbers are correctly identified"""
        # Test all defined numbers. Should be True
        for i in self.numbers:
            self.assertTrue(validate.is_number(i))
        # Test all defined numbers to be vowels or consonants. Should
        # be False
        for i in self.vowels + self.consonants:
            self.assertFalse(validate.is_number(i))

    def test_is_vowel(self):
        """Test that vowels are correctly identified"""
        # Test all defined vowels. Should be True
        for i in self.vowels + self.vowels.upper():
            self.assertTrue(validate.is_vowel(i))
        # Test all defined consonants to be vowels or numbers. Should
        # be False
        for i in self.consonants + self.numbers:
            self.assertFalse(validate.is_vowel(i))

    def test_is_punctuation(self):
        """Test that punctuations are correctly identified

        Anything that is neither a number, nor vowel nor consonant is
        identified as a punctuation.

        """
        for i in '`~!@#$%^&*()-_=+\\|[{}]\'",<.>/?':
            self.assertTrue(validate.is_punctuation(i))
            self.assertFalse(validate.is_vowel(i))
            self.assertFalse(validate.is_consonant(i))
            self.assertFalse(validate.is_number(i))

    def test_fix_string_case(self):
        """Test phonetic-compatible case-transformations of strings

        This ensures validate.fix_strings function works as
        expected. It should properly change text to lowercase but
        retain case-sensitive characters defined in config as
        uppercase.
        """
        # 'ABOL taBOL' should become 'abOl tabOl'
        self.assertEquals(validate.fix_string_case('ABOL taBOl'),
                          'abOl tabOl')
        # 'KhiCuRi' should become 'khicuRi'
        self.assertEquals(validate.fix_string_case('KhiCuRi'),
                          'khicuRi')
        # 'KaTh-BuRO' should become 'kaTh-buRO'
        self.assertEquals(validate.fix_string_case('KaTh-BuRO'),
                          'kaTh-buRO')
        # 'raMgoRurer Chana' should become 'ramgoRurer chana'
        self.assertEquals(validate.fix_string_case('raMgoRurer Chana'),
                          'ramgoRurer chana')

    def test_is_exact(self):
        """Test exact search response of needle in haystack"""
        self.assertTrue(validate.is_exact('abcd', 'abcdefgh', 0, 4, False))
        self.assertFalse(validate.is_exact('abcd', 'abcdefgh', 0, 4, True))
        self.assertFalse(validate.is_exact('bcd', 'abcdefgh', 0, 4, False))
        self.assertTrue(validate.is_exact('bcd', 'abcdefgh', 0, 4, True))
        # Test with substring out of string's range
        self.assertFalse(validate.is_exact('a', 'a', 1, 2, False))
        self.assertTrue(validate.is_exact('a', 'a', 1, 2, True))
