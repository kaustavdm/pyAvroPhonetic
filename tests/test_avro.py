#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides test cases for pyavrophonetic.avro

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
from pyavrophonetic import avro
from pyavrophonetic.config import AVRO_DICT
from pyavrophonetic.utils import utf


class TestAvro(unittest.TestCase):
    """Tests parsing methods for pyavrophonetic.avro"""

    def test_patterns_without_rules_from_config(self):
        """Tests all patterns from config that don't have rules"""
        for pattern in AVRO_DICT['data']['patterns']:
            if 'rules' not in pattern:
                self.assertEquals(pattern['replace'],
                                  avro.parse(pattern['find']))

    def test_patterns_without_rules_not_from_config(self):
        """Tests all patterns not from config that don't have rules

        This test is done in addition to
        test_patterns_without_rules_from_config() to ensure that text
        passed manually to avro.parse are properly parsed when they
        don't exact match a pattern that has no rules specified.

        """
        # Test some conjunctions
        self.assertEquals(utf("ভ্ল"), avro.parse("bhl"))
        self.assertEquals(utf("ব্ধ"), avro.parse("bdh"))
        self.assertEquals(utf("ব্ধ"), avro.parse("bdh"))
        self.assertEquals(utf("ড্ড"), avro.parse("DD"))
        # stunned stork!
        self.assertEquals(utf("স্তব্ধ বক"),
                          avro.parse("stbdh bk"))

    def test_patterns_numbers(self):
        """Test patterns - numbers"""
        # Test some numbers
        self.assertEquals(utf("০"), avro.parse("0"))
        self.assertEquals(utf("১"), avro.parse("1"))
        self.assertEquals(utf("২"), avro.parse("2"))
        self.assertEquals(utf("৩"), avro.parse("3"))
        self.assertEquals(utf("৪"), avro.parse("4"))
        self.assertEquals(utf("৫"), avro.parse("5"))
        self.assertEquals(utf("৬"), avro.parse("6"))
        self.assertEquals(utf("৭"), avro.parse("7"))
        self.assertEquals(utf("৮"), avro.parse("8"))
        self.assertEquals(utf("৯"), avro.parse("9"))
        self.assertEquals(utf("১১২"), avro.parse("112"))

    def test_patterns_punctuations(self):
        """Tests patterns - punctuations"""
        # Test some punctuations
        self.assertEquals(utf("।"), avro.parse("."))
        self.assertEquals(utf("।।"), avro.parse(".."))
        self.assertEquals(utf("..."), avro.parse("..."))

    def test_patterns_with_rules_svaravarna(self):
        """Test patterns - with rules - svaravarna"""
        # Test some numbers
        self.assertEquals(utf("অ"), avro.parse("o"))
        self.assertEquals(utf("আ"), avro.parse("a"))
        self.assertEquals(utf("ই"), avro.parse("i"))
        self.assertEquals(utf("ঈ"), avro.parse("I"))
        self.assertEquals(utf("উ"), avro.parse("u"))
        self.assertEquals(utf("উ"), avro.parse("oo"))
        self.assertEquals(utf("ঊ"), avro.parse("U"))
        self.assertEquals(utf("এ"), avro.parse("e"))
        self.assertEquals(utf("ঐ"), avro.parse("OI"))
        self.assertEquals(utf("ও"), avro.parse("O"))
        self.assertEquals(utf("ঔ"), avro.parse("OU"))

    def test_non_ascii(self):
        """Test parser response for non ascii characters

        Parser should return any non-ascii characters passed to it

        """
        self.assertEquals(utf('ব'), avro.parse('ব'))
        self.assertEquals(utf('অভ্র'), avro.parse('অভ্র'))
        # mixed string
        self.assertEquals(utf('বআবা গো'), avro.parse('বaba gO'))
        self.assertEquals(utf('আমি বাংলায় গান গাই'),
                          avro.parse('aমি বাংলায় gaন গাi'))

    def test_words_with_punctuations(self):
        """Test parsing of words with punctuations"""
        self.assertEquals(utf('আয়রে,'), avro.parse('ayre,'))
        self.assertEquals(utf('ভোলা'), avro.parse('bhOla'))
        self.assertEquals(utf('খেয়াল'), avro.parse('kheyal'))
        self.assertEquals(utf('খোলা'), avro.parse('khOla'))

    def test_sentences(self):
        """Test parsing of sentences"""
        self.assertEquals(utf('আমি বাংলায় গান গাই'),
                          avro.parse('ami banglay gan gai'))
