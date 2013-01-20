#!/usr/bin/env python

"""Provides count functions for pyAvroPhonetic

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


def count_vowels(text):
    """Count number of occurrences of vowels in a given string"""
    count = 0
    for i in text:
        if i.lower() in config.AVRO_VOWELS:
            count += 1
    return count

def count_consonants(text):
    """Count number of occurrences of consonants in a given string"""
    count = 0
    for i in text:
        if i.lower() in config.AVRO_CONSONANTS:
            count += 1
    return count
