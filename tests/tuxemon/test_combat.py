# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2025 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
import unittest
import pygame
from unittest.mock import MagicMock
from tuxemon.states.combat.combat import CombatState
from tuxemon.npc import NPC
from tuxemon.battle import Battle
from tuxemon.monster import Monster

class TestCombat(unittest.TestCase):

    def setUp(self):
        # Mock dependencies for CombatState
        self.mock_graphics = MagicMock(name="mock_graphics")
        self.mock_player = MagicMock(spec=NPC, name="Player")
        self.mock_npc = MagicMock(spec=NPC, name="NPC")
        self.mock_monster = MagicMock(spec=Monster, name="Monster")

        # Set up mock monster properties
        self.mock_monster.hp = 50
        self.mock_monster.name = "TestMonster"

        # Create instance of CombatState
        self.combat_state = CombatState(
            players=(self.mock_player, self.mock_npc),
            graphics=None,  # Graphics is no longer needed for this test
            combat_type="trainer",
        )

    def test_combat_state_initialization(self):
        """Test that the CombatState initializes properly."""
        self.assertEqual(len(self.combat_state.players), 2)
        self.assertFalse(self.combat_state.is_trainer_battle is None)
        self.assertTrue(self.combat_state.is_trainer_battle)

    def test_add_monster_to_battle(self):
        """Test adding a monster to the battle."""
        self.combat_state.monsters_in_play[self.mock_player].append(self.mock_monster)

        # Assertions
        self.assertIn(self.mock_monster, self.combat_state.monsters_in_play[self.mock_player])
        self.assertEqual(
            self.combat_state.monsters_in_play[self.mock_player][0].name,
            "TestMonster"
        )

    def test_monster_faint(self):
        """Test that fainting a monster updates correctly."""
        self.mock_monster.hp = 0  # Simulate the HP dropping to 0
        self.assertEqual(self.mock_monster.hp, 0)

        # Simulate fainting behavior
        self.combat_state.monsters_in_play[self.mock_player].append(self.mock_monster)
        self.combat_state.monsters_in_play[self.mock_player].remove(self.mock_monster)

        # Assertions
        self.assertNotIn(self.mock_monster, self.combat_state.monsters_in_play[self.mock_player])

    def tearDown(self):
        """Clean up after tests."""
        self.combat_state = None
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
