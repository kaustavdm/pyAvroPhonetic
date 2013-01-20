#!/usr/bin/env python

"""Provides test cases for pyavrophonetic.avro.utils.count

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
from pyavrophonetic.utils import count


class TestUtilsCount(unittest.TestCase):
    """Tests validation methods for pyavrophonetic.utils.count"""

    def test_count_vowels(self):
        """Test vowel count in a given string"""
        self.assertEquals(count.count_vowels('haTTima Tim Tim'), 5)
        self.assertEquals(count.count_vowels('tara maThe paRe Dim'), 7)
        self.assertEquals(count.count_vowels('tader mathay duTO sing'), 7)
        self.assertEquals(count.count_vowels('tara haTTima Tim Tim'), 7)

    def test_count_consonants(self):
        """Test consonant count in a given string"""
        self.assertEquals(count.count_consonants('ei dekh pensil'), 7)
        self.assertEquals(count.count_consonants('nOTbuk e hate'), 6)
        self.assertEquals(count.count_consonants('ei dekh bhora sob'), 8)
        self.assertEquals(count.count_consonants('kil`bil lekha te'), 8)
