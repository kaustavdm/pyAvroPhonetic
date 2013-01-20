#!/usr/bin/env python

"""Provides validation functions for pyAvroPhonetic

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


def is_vowel(text):
    """Check if given string is a vowel"""
    if text.lower().encode('utf-8') in config.AVRO_VOWELS:
        return True
    else:
        return False

def is_consonant(text):
    """Check if given string is a consonant"""
    if text.lower().encode('utf-8') in config.AVRO_CONSONANTS:
        return True
    else:
        return False

def is_number(text):
    """Check if given string is a number"""
    if text.lower().encode('utf-8') in config.AVRO_NUMBERS:
        return True
    else:
        return False

def is_punctuation(text):
    """Check if given string is a punctuation"""
    text = text.lower().encode('utf-8')
    if (text in config.AVRO_VOWELS or
        text in config.AVRO_CONSONANTS or
        text in config.AVRO_NUMBERS):
        return False
    else:
        return True

def is_case_sensitive(text):
    """Check if given string is case sensitive"""
    if text.lower().encode('utf-8') in config.AVRO_CASESENSITIVES:
        return True
    else:
        return False

def fix_string_case(text):
    """Converts case-insensitive characters to lower case

    Case-sensitive characters as defined in config.AVRO_CASESENSITIVES
    retain their case, but others are converted to their lowercase
    equivalents. The result is a string with phonetic-compatible case
    which will the parser will understand without confusion.
    """
    fixed = []
    for i in text:
        if is_case_sensitive(i):
            fixed.append(i)
        else:
            fixed.append(i.lower())
    return ''.join(fixed)
