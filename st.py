#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
this is used for grouping every saving throw in only one place
"""


class SavingThrows(object):

    """
    facility to manipulate saving throws.
    """

    def __init__(self, value=None):
        """
        Some saving throw class is split because they may have bonus coming from different sources (e.g. dwarf's racial bonus to poison and magic)
        """

        self.rod = value[0]
        self.staff = value[0]
        self.wand = value[0]
        self.breath_weapon = value[1]
        self.death = value[2]
        self.paralysis = value[2]
        self.poison = value[2]
        self.petrification = value[3]
        self.polymorph = value[3]
        self.spell = value[4]


