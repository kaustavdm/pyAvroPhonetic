#!/usr/bin/env python

"""Provides validation and count utilities for pyAvroPhonetic

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
from pyavrophonetic import config


class Validate:
    """Provides validation methods for pyAvroPhonetic"""

    def __init__(self):
        """Initialize the Validate class"""
        # Provide easy access to last fixed string
        self.fixed_string = ''

    def is_vowel(self, text):
        """Check if given string is a vowel"""
        if text.lower().encode('utf-8') in config.AVRO_VOWELS:
            return True
        else:
            return False

    def is_consonant(self, text):
        """Check if given string is a consonant"""
        if text.lower().encode('utf-8') in config.AVRO_CONSONANTS:
            return True
        else:
            return False

    def is_number(self, text):
        """Check if given string is a number"""
        if text.lower().encode('utf-8') in config.AVRO_NUMBERS:
            return True
        else:
            return False

    def is_punctuation(self, text):
        """Check if given string is a punctuation"""
        text = text.lower().encode('utf-8')
        if (text in config.AVRO_VOWELS or
            text in config.AVRO_CONSONANTS or
            text in config.AVRO_NUMBERS):
            return False
        else:
            return True

    def is_case_sensitive(self, text):
        """Check if given string is case sensitive"""
        if text.lower().encode('utf-8') in config.AVRO_CASESENSITIVES:
            return True
        else:
            return False

    def fix_string(self, text):
        """Implement fix string method"""
        fixed = []
        for i in text:
            if self.is_case_sensitive(i):
                fixed.append(i)
            else:
                fixed.append(i.lower())
        self.fixed_string = ''.join(fixed)
        return self.fixed_string


class Count:
    """Provides methods for counting certain occurrences in string"""

    def __init__(self):
        """Initialize Count class"""
        # Provide easy access to last count number
        self.count = 0

    def count_vowels(self, text):
        """Count number of occurrences of vowels in a given string"""
        count = 0
        for i in text:
            if i in config.AVRO_VOWELS:
                count += 1
        self.count = count
        return count

    def count_consonants(self, text):
        """Count number of occurrences of consonants in a given string"""
        count = 0
        for i in text:
            if i in config.AVRO_CONSONANTS:
                count += 1
        self.count = count
        return count
