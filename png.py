#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
pngs manages png creation
"""

from race import Race, Dwarf
from profession import Profession, Fighter
from ability import *
from config import *
from tes import rnd
import pdb


class FighterGenerator:

    """
    Builder for class fighter
    """

    @staticmethod
    def create(**kwargs):
        """
        default procedure for give birth to a fighter
        """

        return Fighter(level=kwargs.get('level', 1))


class DwarfGenerator:

    """
    Builder for Dwarf class. Note that it's necessary an ability row in order to instantiate it.
    """

    @staticmethod
    def create(**kwargs):
        """
        default procedure for give birth to a dwarf
        """

        generator = AbilityGeneratorFactory()
        abilities = generator.create(method=kwargs.get('generator',
                BEST_OF_THREE), profession=kwargs.get('profession'))
        return Dwarf(abilities, kwargs['st'])


class PngModelFactory:

    def create(self, **kwargs):
        """
        Initial release for creating a fighter/dwarf
        """

        if kwargs['profession'] == FIGHTER:
            profession = FighterGenerator.create(**kwargs)
        if kwargs['race'] == DWARF:
            race = DwarfGenerator.create(st=profession.st(),
                    generator=kwargs.get('generator'))
        m = PngModel(race, profession)
        m.create()
        return m


class PngModel:

    """
    Wraps a race and a class. mVc
    """

    def __init__(self, race, profession):
        profession.create()
        self.race = race
        self.profession = profession
        self._hp = 0

    def create(self):
        """
        put here initialization for stats that need both a race and a profession
        """

        self._calculate_hp()
        self.race.alterAbilities()
        self.race.racialAbilities()

    def _calculate_hp(self):
        """
        TODO: better use a list so that it can maintain an history of abilities
        """

        self._hp = rnd(self.profession.level_advancement()[HIT_DICE],
                       self.profession.dice(),
                       self.ability(CONSTITUTION).bonus()[HIT_POINTS_BONUS]) \
            + self.profession.level_advancement()[HP_AFTER_TITLE_LEVEL]

    def ability(self, ability):
        """
        this is only a shortcut
        """

        return self.race.abilities.get(ability)


class PngController:

    """
    mvC 
    """

    def __init__(self):
        self.factory = PngModelFactory()
        self.view = PngView()

    def main(self, **kwargs):
        png = self.factory.create(**kwargs)
        self.view.display(png)


class PngView:

    """
    mVc
    """

    def display(self, item):
        """
        TODO: this is temporary and will be extracted in near future.
        """

        print '%s %s %d' % (item.race.race_name,
                            item.profession._profession_name,
                            item.profession.level)
        print 'Hp %d' % item._hp
        print 'str %s des %s cos %s int %s wis %s car %s' % (
            item.ability(STRENGTH).value(),
            item.ability(DEXTERITY).value(),
            item.ability(CONSTITUTION).value(),
            item.ability(INTELLIGENCE).value(),
            item.ability(WISDOM).value(),
            item.ability(CHARISMA).value(),
            )
        for i in [
            STRENGTH,
            DEXTERITY,
            CONSTITUTION,
            INTELLIGENCE,
            WISDOM,
            CHARISMA,
            ]:
            print str.join(', ', ['%s: %s' % (r,
                           item.ability(i).bonus()[r]) for r in
                           item.ability(i).bonus()])
        print 'number of attacks %s round' % item.profession._n_attack
        print 'class abilities: %s' \
            % ''.join(item.profession.profession_abilities)
        print 'weapon proficiency %d' \
            % item.profession._weapon_proficiency
        print 'weapon malus with no proficiency %+d' \
            % item.profession._non_proficiency
        print 'saving throws'
        print 'rod, staff & wand %d breath weapon: %d ' \
            % (item.race.ts.rod, item.race.ts.breath_weapon)
        if item.race.ts.poison == item.race.ts.death:
            print 'death, paralysis & poison %d' % item.race.ts.death
        else:
            print 'death %d, paralysis %d, poison %d' \
                % (item.race.ts.death, item.race.ts.paralysis,
                   item.race.ts.poison)
        print 'petrification %d, polymorph %d' \
            % (item.race.ts.petrification, item.race.ts.polymorph)
        print 'spell %d' % item.race.ts.spell
        print 'base thaco %d' % item.profession.thac0()
        print 'to hit table '
        x=item.profession.thac()
        min,max=-10,10
        for i in range (min,max):
            print '%4d ' %i , 
        print
        for i in range (min,max):
            print '%4d ' %x[i] , 


pg = PngController()

pg.main(level=3, profession=FIGHTER, race=DWARF,
        generator=BEST_OF_THREE)
