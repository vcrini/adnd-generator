#!/usr/bin/python
# -*- coding: utf-8 -*-

from ability import Abilities, Ability
from config import *
from dice import rnd
from st import SavingThrows


class ProfessionException(Exception):

    pass


class Profession(object):

    def __init__(self, **kwargs):
        self._max_level = 36
        self._weapon_specialization = False
        self.level = kwargs['level']
        self._min_abilities = Abilities(
            strength=3,
            intelligence=3,
            wisdom=3,
            constitution=3,
            charisma=3,
            dexterity=3,
            )
        self._px_min_abilities = None
        self._weapon_permitted = None
        self._armor_permitted = None
        self._n_attack = '1/1'
        self._profession_name = self.__class__.__name__

    def create(self):
        self._class_abilities()

    def raiseE(self, text):
        raise ProfessionException('%s for %s' % (text,
                                  str(self.__class__)))

    def st(self):
        raise self.RaiseE('saving throws not defined')

    def dice(self):
        raise self.RaiseE('dice not defined')

    def _class_abilities(self):
        raise self.RaiseE('class abilities not defined')

    def _title_level(self):
        raise self.RaiseE('title level not defined')

    def level_advancement(self):
        raise self.RaiseE('level advancement not implemented')

    def twenty_to_hit(self):
        raise self.RaiseE('twenty to hit not defined')

    def thacx(self, x=0):
        """
        To hit armoring class x
        20 is a valid hit to roll armor class until ac is too lop
        """

        y = self.thac0() - x

        if y < 21:
            return y
        elif 21 <= y < 26:
            return 20
        else:
            return y - 6

    def thac(self):
        """
        returns hash with key representing armoring class and value hit needed
        """

        x = {}
        for i in range(-10, 10):
            x[i] = self.thacx(i)
        return x

    def thac0(self):

        return 21 + self.twenty_to_hit()


class Fighter(Profession):

    def __init__(self, **kwargs):

        super(Fighter, self).__init__(**kwargs)

        self._min_abilities = Abilities(
            strength=9,
            intelligence=3,
            wisdom=6,
            constitution=7,
            charisma=6,
            dexterity=6,
            )
        self._px_min_abilities = Abilities(
            strength=16,
            intelligence=3,
            wisdom=3,
            constitution=3,
            charisma=3,
            dexterity=3,
            )
        self._non_proficiency = -2
        self._weapon_proficiency = 4 + int(self.level / 2)
        self._weapon_specialization = True

    def dice(self):
        return 10

    def _title_level(self):
        return 9

    def _class_abilities(self):
        if 7 <= self.level <= 12:
            self._n_attack = '3/2'
        elif self.level > 12:
            self._n_attack = '2/1'
        if self._weapon_specialization:
            if 1 <= self.level <= 7:
                self._n_attack = '3/2'
            if 7 <= self.level <= 12:
                self._n_attack = '2/1'
            else:
                self._n_attack = '5/2'
        self.profession_abilities = ['fight the unskilled']

    def level_advancement(self):
        adv = {
            1: [0, 1, 0],
            2: [1900, 2, 0],
            3: [4250, 3, 0],
            4: [7750, 4, 0],
            5: [16000, 5, 0],
            6: [35000, 6, 0],
            7: [75000, 7, 0],
            8: [125000, 8, 0],
            9: [250000, 9, 0],
            10: [500000, 9, 3],
            11: [750000, 9, 6],
            }
        try:
            z = adv[self.level]
        except KeyError:
            z = [750000 + (self.level - 11) * 250000, 9, (self.level
                 - 9) * 3]
        return {PX: z[0], HIT_DICE: z[1], HP_AFTER_TITLE_LEVEL: z[2]}

    def st(self):
        x = self.level
        z = None
        if x == 0:
            z = [18, 20, 16, 17, 19]
        elif 1 <= x <= 2:
            z = [16, 17, 14, 15, 17]
        elif 3 <= x <= 4:
            z = [15, 16, 13, 14, 16]
        elif 5 <= x <= 6:
            z = [13, 13, 11, 12, 14]
        elif 7 <= x <= 8:
            z = [12, 12, 10, 11, 13]
        elif 9 <= x <= 10:
            z = [10, 9, 8, 9, 11]
        elif 11 <= x <= 12:
            z = [9, 8, 7, 8, 10]
        elif 13 <= x <= 14:
            z = [7, 5, 5, 6, 8]
        elif 15 <= x <= 16:
            z = [6, 4, 4, 5, 7]
        elif 17 <= x <= 18:
            z = [5, 4, 3, 4, 6]
        else:
            z = [4, 3, 2, 3, 5]
        return SavingThrows(z)

    def twenty_to_hit(self):
        return 1 - self.level


