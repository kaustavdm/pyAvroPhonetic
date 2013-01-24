#!/usr/bin/env python

"""Provides the main library for Avro Phonetic

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
from pyavrophonetic.utils import validate
from pyavrophonetic.utils import utf
from pyavrophonetic import config


# Constants
PATTERNS = config.AVRO_DICT['data']['patterns']
NON_RULE_PATTERNS = [p for p in PATTERNS if 'rules' not in p]
RULE_PATTERNS = [p for p in PATTERNS if 'rules' in p]

def parse(text):
    """Parses input text, matches and replaces using avrodict

    If a valid replacement is found, returns the replaced string. If
    no replacement is found, returns the input text.

    Usage:

    ::
      from pyavrophonetic import avro
      avro.parse("ami banglay gan gai")

    """
    # Sanitize text case to meet phonetic comparison standards
    fixed_text = validate.fix_string_case(utf(text))
    # prepare output list
    output = []
    # cursor end point
    cur_end = 0
    # iterate through input text
    for cur, i in enumerate(fixed_text):
        # Trap characters with unicode encoding errors
        try:
            i.encode('utf-8')
        except UnicodeDecodeError:
            uni_pass = False
        else:
            uni_pass = True
        # Default value for match
        match = {'matched': False}
        # Check cur is greater than or equals cur_end. If cursor is in
        # a position that has alread been processed/replaced, we don't
        # process anything at all
        if not uni_pass:
            cur_end = cur + 1
            output.append(i)
        elif cur >= cur_end and uni_pass:
            # Try looking in non rule patterns with current string portion
            match = match_non_rule_patterns(fixed_text, cur)
            # Check if non rule patterns have matched
            if match["matched"]:
                output.append(match["replaced"])
                cur_end = cur + len(match["found"])
            else:
            # if non rule patterns have not matched, try rule patterns
                match = match_rule_patterns(fixed_text, cur)
                # Check if rule patterns have matched
                if match["matched"]:
                    # Update cur_end as cursor + length of match found
                    cur_end =  cur + len(match["found"])
                    # Process its rules
                    replaced = process_rules(rules = match["rules"],
                                             fixed_text = fixed_text,
                                             cur = cur, cur_end = cur_end)
                    # If any rules match, output replacement from the
                    # rule, else output it's default top-level/default
                    # replacement
                    if replaced is not None:
                        # Rule has matched
                        output.append(replaced)
                    else:
                        # No rules have matched
                        # output common match
                        output.append(match["replaced"])

            # If none matched, append present cursor value
            if not match["matched"]:
                cur_end = cur + 1
                output.append(i)

    # End looping through input text and produce output
    return ''.join(output)

def match_non_rule_patterns(fixed_text, cur=0):
    """Matches given text at cursor position with non rule patterns

    Returns a dictionary of three elements:

    - "matched" - Bool: depending on if match found
    - "found" - string/None: Value of matched pattern's 'find' key or none
    - "replaced": string Replaced string if match found else input string at
    cursor

     """
    pattern = exact_find_in_pattern(fixed_text, cur, NON_RULE_PATTERNS)
    if len(pattern) > 0:
        return {"matched": True, "found": pattern[0]['find'],
                "replaced": pattern[0]['replace']}
    else:
        return {"matched": False, "found": None,
                "replaced": fixed_text[cur]}

def match_rule_patterns(fixed_text, cur=0):
    """Matches given text at cursor position with rule patterns

    Returns a dictionary of four elements:

    - "matched" - Bool: depending on if match found
    - "found" - string/None: Value of matched pattern's 'find' key or none
    - "replaced": string Replaced string if match found else input string at
    cursor
    - "rules": dict/None: A dict of rules or None if no match found

    """
    pattern = exact_find_in_pattern(fixed_text, cur, RULE_PATTERNS)
    # if len(pattern) == 1:
    if len(pattern) > 0:
        return {"matched": True, "found": pattern[0]['find'],
                "replaced": pattern[0]['replace'], "rules": pattern[0]['rules']}
    else:
        return {"matched": False, "found": None,
                "replaced": fixed_text[cur], "rules": None}

def exact_find_in_pattern(fixed_text, cur=0, patterns=PATTERNS):
    """Returns pattern items that match given text, cur position and pattern"""
    return [x for x in patterns if (cur + len(x['find']) <= len(fixed_text))
             and x['find'] == fixed_text[cur:(cur + len(x['find']))]]

def process_rules(rules, fixed_text, cur = 0, cur_end = 1):
    """Process rules matched in pattern and returns suitable replacement

    If any rule's condition is satisfied, output the rules "replace",
    else output None

    """
    replaced = ''
    # iterate through rules
    for rule in rules:
        matched = False
        # iterate through matches
        for match in rule['matches']:
            matched = process_match(match, fixed_text, cur, cur_end)
            # Break out of loop if we dont' have a match. Here we are
            # trusting avrodict to have listed matches sequentially
            if not matched:
                break
        # If a match is found, stop looping through rules any further
        if matched:
            replaced = rule['replace']
            break

    # if any match has been found return replace value
    if matched:
        return replaced
    else:
        return None

def process_match(match, fixed_text, cur, cur_end):
    """Processes a single match in rules"""
    # Set our tools
    # -- Initial/default value for replace
    replace = True
    # -- Set check cursor depending on match['type']
    if match['type'] == 'prefix':
        chk = cur - 1
    else:
        # suffix
        chk = cur_end
    # -- Set scope based on whether scope is negative
    if match['scope'].startswith('!'):
        scope = match['scope'][1:]
        negative = True
    else:
        scope = match['scope']
        negative = False

    # Let the matching begin
    # -- Punctuations
    if scope == 'punctuation':
        # Conditions: XORd with negative
        if (not ((chk < 0 and match['type'] == 'prefix') or
                 (chk >= len(fixed_text) and match['type'] == 'suffix') or
                 validate.is_punctuation(fixed_text[chk]))
            ^ negative):
            replace = False
    # -- Vowels -- Checks: 1. Cursor should not be at first character
    # -- if prefix or last character if suffix, 2. Character at chk
    # -- should be a vowel. 3. 'negative' will invert the value of 1
    # -- AND 2
    elif scope == 'vowel':
        if (not (((chk >= 0 and match['type'] == 'prefix') or
                  (chk < len(fixed_text) and match['type'] == 'suffix'))
                 and validate.is_vowel(fixed_text[chk]))
            ^ negative):
            replace =  False
    # -- Consonants -- Checks: 1. Cursor should not be at first
    # -- character if prefix or last character if suffix, 2. Character
    # -- at chk should be a consonant. 3. 'negative' will invert the
    # -- value of 1 AND 2
    elif scope == 'consonant':
        if (not (((chk >= 0 and match['type'] == 'prefix') or
                  (chk < len(fixed_text) and match['type'] == 'suffix'))
                 and validate.is_consonant(fixed_text[chk]))
            ^ negative):
            replace = False
    # -- Exacts
    elif scope == 'exact':
        # Prepare cursor for exact search
        if match['type'] == 'prefix':
            exact_start = cur - len(match['value'])
            exact_end = cur
        else:
            # suffix
            exact_start = cur_end
            exact_end = cur_end + len(match['value'])
        # Validate exact find.
        if not validate.is_exact(match['value'], fixed_text, exact_start,
                                 exact_end, negative):
            replace = False
    # Return replace, which will be true if none of the checks above match
    return replace
