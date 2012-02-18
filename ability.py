#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
manages al things related to abilities
"""
import re
import pdb
from config import *
from tes import rnd, rnd2


class Ability(object):
    """
    Base class
    """

    def __init__(self, value=None):
        self._value = None
        self.value(value)

    def value(self, value=None):
        """
        setter & getter
        """
        if value:
            self._value = value
        return self._value

    def bonus(self):
        """
        to be implemented in sons
        """
        raise NameError('This must defined in derived class because depends on ability type.'
                        )

    def b(self, singular_bonus):
        """
        facility to quickly access to single bonus item
        """

        return self.bonus()[singular_bonus]


class Strength(Ability):
    """
    How strong one is
    """

    def __init__(self, value=None):
        self._hundreds = None
        super(Strength, self).__init__(value)
        self.data = {
            '3': [-3, -1, -35, 1, 0],
            '4': [-2, -1, -25, 1, 0],
            '5': [-2, -1, -25, 1, 0],
            '6': [-1, 0, -15, 1, 0],
            '7': [-1, 0, -15, 1, 0],
            '8': [0, 0, 0, 2, 1],
            '9': [0, 0, 0, 2, 1],
            '10': [0, 0, 0, 2, 2],
            '11': [0, 0, 0, 2, 2],
            '12': [0, 0, 10, 2, 4],
            '13': [0, 0, 10, 2, 4],
            '14': [0, 0, 20, 2, 7],
            '15': [0, 0, 20, 2, 7],
            '16': [0, 1, 35, 3, 10],
            '17': [1, 1, 50, 3, 13],
            '18': [1, 2, 75, 3, 16],
            '18.50': [1, 3, 100, 3, 20],
            '18.75': [2, 3, 125, 4, 25],
            '18.90': [2, 4, 150, 4, 30],
            '18.99': [2, 5, 200, 4, 35],
            '18.001': [3, 6, 300, 5, 40],
            }

    def value(self, value=None):
        """
        I had to reimplement because of extraordinary attribute management
        """
        if value:
            x = re.match(r'18/(\d+)', str(value))
            self._hundreds = 0
            if x:
                self._hundreds = int(x.group(1))
                self._value = 18
            else:
                self._value = value
        if self._hundreds == 0:
            return self._value
        else:
            return '18/%02d' % self._hundreds

    def value_no_hundreds(self):
        """
        returns value without extraordinary "part"
        """
        return self._value

    def bonus(self):
        """
        different way to calculate bonus caused by extraordinary "part"
        """
        #pdb.set_trace()
        y = self.data
        if self._hundreds==0:
            x = str(self.value())
        else:
            if self._hundreds == 100:
                x = '18.001'
            elif self._hundreds < 51:
                x = '18.50'
            elif self._hundreds < 91:
                x = '18.90'
            elif self._hundreds <= 99:
                x = '18.99'
            else:
                raise NameError('Strength value %s not valid'
                                % self.value())
        return {
            BONUS_TO_HIT: y[x][0],
            BONUS_TO_DAMAGE: y[x][1],
            ENCUMBRANCE_ADJUSTMENT: y[x][2],
            MINOR_TEST: y[x][3],
            MAJOR_TEST: y[x][4],
            }


class Dexterity(Ability):
    """
    how agile he is.
    """
    def __init__(self, value=None):
        super(Dexterity, self).__init__(value)
        self.data = {
            '3': [-3, -3, 4],
            '4': [-2, -2, 3],
            '5': [-1, -1, 2],
            '6': [0, 0, 1],
            '7': [0, 0, 0],
            '8': [0, 0, 0],
            '9': [0, 0, 0],
            '10': [0, 0, 0],
            '11': [0, 0, 0],
            '12': [0, 0, 0],
            '13': [0, 0, 0],
            '14': [0, 0, 0],
            '15': [0, 0, -1],
            '16': [1, 1, -2],
            '17': [2, 2, -3],
            '18': [3, 3, -4],
            '19': [3, 3, -4],
            }

    def bonus(self):
        x = str(self.value())
        y = self.data
        return {SURPRISE_BONUS: y[x][0], MISSILE_BONUS_TO_HIT: y[x][1],
                AC_ADJUSTMENT: y[x][2]}


class Constitution(Ability):
    """
    I drink many beers!
    """

    def __init__(self, value=None):
        super(Constitution, self).__init__(value)
        self.data = {
            '3': [-2, 40, 35],
            '4': [-1, 45, 40],
            '5': [-1, 50, 45],
            '6': [-1, 55, 50],
            '7': [0, 60, 55],
            '8': [0, 65, 60],
            '9': [0, 70, 65],
            '10': [0, 75, 70],
            '11': [0, 80, 75],
            '12': [0, 85, 80],
            '13': [0, 90, 85],
            '14': [0, 92, 88],
            '15': [1, 94, 91],
            '16': [2, 96, 95],
            '17': [2, 98, 97],
            '18': [2, 100, 99],
            '19': [2, 100, 99],
            }

    def bonus(self):
        x = str(self.value())
        y = self.data
        return {HIT_POINTS_BONUS: y[x][0], RAISE_DEAD: y[x][1],
                SYSTEM_SHOCK: y[x][2]}


class ConstitutionWarrior(Constitution):
    """
    Warriors have more hp
    """
    def __init__(self, value=None):
        Constitution.__init__(self, value)
        self.data['17'][0] = 3
        self.data['18'][0] = 4
        self.data['19'][0] = 5


class Intelligence(Ability):
    """
    10^10
    """
    def __init__(self, value=None):
        super(Intelligence, self).__init__(value)
        self.data = {
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 1,
            '9': 1,
            '10': 2,
            '11': 2,
            '12': 3,
            '13': 3,
            '14': 4,
            '15': 4,
            '16': 5,
            '17': 6,
            '18': 7,
            '19': 8,
            }

    def bonus(self):
        return {MAXIMUM_ADDITIONAL_LANGUAGES: self.data[str(self.value())]}


class Wisdom(Ability):
    """
    Stupid is who behaves like a stupid
    """
    def __init__(self, value=None):
        super(Wisdom, self).__init__(value)
        self.data = {
            '3': -3,
            '4': -2,
            '5': -1,
            '6': -1,
            '7': -1,
            '8': 0,
            '9': 0,
            '10': 0,
            '11': 0,
            '12': 0,
            '13': 0,
            '14': 0,
            '15': 1,
            '16': 2,
            '17': 3,
            '18': 4,
            '19': 5,
            }

    def bonus(self):
        return {MENTAL_SAVING_THROW_BONUS: self.data[str(self.value())]}


class Charisma(Ability):
    """
    Mirror of my kingdom how is [...]
    """
    def __init__(self, value=None):
        super(Charisma, self).__init__(value)
        self.data = {
            '3': [1, -30, -25],
            '4': [1, -25, -20],
            '5': [2, -20, -15],
            '6': [2, -15, -10],
            '7': [3, -10, -5],
            '8': [3, -5, 0],
            '9': [4, 0, 0],
            '10': [4, 0, 0],
            '11': [4, 0, 0],
            '12': [5, 0, 0],
            '13': [5, 0, 5],
            '14': [6, 5, 10],
            '15': [7, 15, 15],
            '16': [8, 20, 25],
            '17': [10, 30, 30],
            '18': [15, 40, 35],
            '19': [20, 50, 40],
            }

    def bonus(self):
        x = str(self.value())
        y = self.data
        return {MAXIMUM_HENCHMEN: y[x][0], LOYALTY_BONUS: y[x][1],
                REACTION_BONUS: y[x][2]}


class Abilities:
    """
    glueing all them together
    """
    def __init__(self, **ability):
        self._value = {
            STRENGTH: Strength(ability[STRENGTH]),
            INTELLIGENCE: Intelligence(ability[INTELLIGENCE]),
            WISDOM: Wisdom(ability[WISDOM]),
            CONSTITUTION: Constitution(ability[CONSTITUTION]),
            DEXTERITY: Dexterity(ability[DEXTERITY]),
            CHARISMA: Charisma(ability[CHARISMA]),
            }

    def get(self, ability=None):
        if ability:
            return self._value[ability]
        else:
            return self._value


class GenericAbilityGenerator:
    """
    calculating with 3d6
    """
    @staticmethod
    def roll():
        return rnd(3, 6)


class BestOfThreeAbilityGenerator:
    """
    calculating with best 3d6 on 4d6
    """
    @staticmethod
    def roll():
        return rnd2(4, 1, 6)


class AbilityGeneratorFactory:
    """
    TODO manage warrior hp
    """
    def create(self, **kwargs):
        if kwargs.get('method') == BEST_OF_THREE:
            x = Abilities(
                strength=self.extraordinary(value=BestOfThreeAbilityGenerator.roll(),
                        profession=kwargs.get('profession')),
                dexterity=BestOfThreeAbilityGenerator.roll(),
                constitution=BestOfThreeAbilityGenerator.roll(),
                wisdom=BestOfThreeAbilityGenerator.roll(),
                intelligence=BestOfThreeAbilityGenerator.roll(),
                charisma=BestOfThreeAbilityGenerator.roll(),
                )
        else:
            x = Abilities(
                strength=self.extraordinary(value=BestOfThreeAbilityGenerator.roll(),
                        profession=kwargs.get('profession')),
                dexterity=GenericAbilityGenerator.roll(),
                constitution=GenericAbilityGenerator.roll(),
                wisdom=GenericAbilityGenerator.roll(),
                intelligence=GenericAbilityGenerator.roll(),
                charisma=GenericAbilityGenerator.roll(),
                )
        return x

    def extraordinary(self, **kw):
        """
        for checking extraordinary strength (e.g. if 18 is rolled and it's a warrior class then check for 18/xx stat)
        """

        if kw['value'] == 18 and kw.get('profession') == 'fighter':
            return '18/%02d' % rnd(1, 100)
        return kw['value']


