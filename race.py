#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
evertthing regarding race
"""

from ability import Ability
from st import SavingThrows
from config import *
import profession
import pdb


class RaceException(Exception):

    """
    So i can know exceptions come from here
    """

    pass


class Race(object):

    """
    Base class
    """

    def __init__(self, abilities, ts):
        self.abilities = abilities
        self.ts = ts
        self.race_name = self.__class__.__name__

    def raiseE(selt, text):
        raise RaceException('%s for %s' % (text, str(self.__class__)))

    def alterAbilities(self):
        self.raiseE('no ability alteration defined')

    def isValid(self):
        self.raiseE('no ability limitation implemented')

    def racialAbilities(self):
        self.raiseE('no ability defined')

    def languages(self):
        self.raiseE('no ability defined')

    def movement(self):
        return 120

    def professionAccessible(self):
        return [
            FIGHTER,
            PALADIN,
            ASSASSIN,
            CLERIC,
            DRUID,
            ILLUSIONIST,
            MAGIC_USER,
            RANGER,
            THIEF,
            ]


class Elf(Race):

    pass


class Dwarf(Race):

    def isValid(self):

        x = self.abilities
        if 8 <= x.get(STRENGTH).value_no_hundreds() <= 18 and 3 \
            <= x.get(DEXTERITY).value() <= 17 and 12 \
            <= x.get(CONSTITUTION).value() <= 19 and 3 \
            <= x.get(INTELLIGENCE).value() <= 18 and 3 \
            <= x.get(WISDOM).value() <= 18 and 3 \
            <= x.get(CHARISMA).value() <= 16:
            return True
        return False

    def alterAbilities(self):
        bonus = int(self.abilities.get(CONSTITUTION).value() / 3.5)
        self.ts.poison = self.ts.poison - bonus
        self.ts.spell = self.ts.spell - bonus
        x = self.abilities
        y = x.get(CONSTITUTION).value()

        # remeber to add a way to not violate max & min values available

        x.get(CONSTITUTION).value(y + 1)
        y = x.get(CHARISMA).value()
        x.get(CHARISMA).value(y - 1)

    def racialAbilities(self):
        return [
            '+1 to hit against goblins, half-orcs, hobgoblins, orc',
            '-4 to AC against giants, ogre, ogre mages, titans and troll'
                ,
            "infravision 60'detect the existence of slopes or grades 75%"
                ,
            'detect the existence of new construction 75%',
            'detect sliding or shifting rooms or walls 66%',
            'detect traps involving stonework 50%',
            'determine depth underground 50%',
            ]

    def languages(self):
        return [
            'dwarfish',
            'gnomish',
            'goblin',
            'kobold',
            'orcish',
            'common tongue',
            ]

    def movement(self):
        return 90

    def professionAccessible(self):
        str = self.abilities.get(STRENGTH).value_no_hundreds
        return {
            FIGHTER: (9 if str >= 18 else (8 if str == 17 else 7)),
            ASSASSIN: 9,
            CLERIC: 8,
            THIEF: UNLIMITED,
            }


