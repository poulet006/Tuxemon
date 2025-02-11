# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2025 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
import unittest
from unittest import mock
from tuxemon.battle import Battle
from tuxemon.monster import Monster

class TestCombat(unittest.TestCase):

    def setUp(self):
        self.battle = Battle()
        self.tuxemon = Monster(name="Testmon", max_hp=10, attack=5, defense=3)
        self.opponent = Monster(name="Foe", max_hp=10, attack=5, defense=3)

    def test_tuxemon_faints_during_battle(self):
        """Test that a Tuxemon properly faints when HP reaches 0"""
        # Deal damage greater than its current HP
        self.tuxemon.take_damage(15)

        # Check if HP is actually 0
        self.assertEqual(self.tuxemon.current_hp, 0)

        # Check if the built-in function recognizes it as fainted
        self.assertTrue(self.tuxemon.is_fainted())

        # Ensure the battle system reacts properly
        self.battle.handle_fainted(self.tuxemon)

        # (Optional) If your system removes fainted Tuxemon from the active battle
        self.assertNotIn(self.tuxemon, self.battle.active_tuxemon)