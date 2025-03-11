# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2025 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
import unittest
from unittest import mock
from tuxemon.db import BattleGraphicsModel
from tuxemon.states.combat.combat import CombatState
from tuxemon.monster import Monster
from tuxemon.npc import NPC
from tuxemon.npc import NPC
from tuxemon.battle import Battle
from tuxemon.monster import Monster

class TestCombat(unittest.TestCase):

    def mockNPC(self) -> None:
        self.monsters = []
        self.isplayer = False
        self.game_variables = {}

    def mockPlayer(self) -> None:
        self.monsters = []
        self.isplayer = True
        self.game_variables = {}

    def seup(self):
        with mock.patch.object(NPC, "__init__", self.mockPlayer()):
            self.mock_player = NPC()
        with mock.patch.object(NPC, "__init__", self.mockNPC()):
            self.mock_npc = NPC()
        self.mock_monster = Monster()
        self.mock_graphics = BattleGraphicsModel()
        self.mock_monster.hp = 50
        self.mock_monster.name = "TestMonster"
        self.mock_player.add_monster(self.mock_monster)

        self.combat_state = CombatState(
            players=(self.mock_player, self.mock_npc),
            graphics=self.mock_graphics,
            combat_type="trainer",
        )
        self.combat_state.isplayer = self.isplayer = True

    def test_combat_state_initialization(self):
        self.assertEqual(len(self.combat_state.players), 2)
        self.assertTrue(self.combat_state.is_trainer_battle)

    def test_add_monster_to_battle(self):
        self.combat_state.monsters_in_play[self.mock_player].append(self.mock_monster)

        self.assertIn(self.mock_monster, self.combat_state.monsters_in_play[self.mock_player])
        self.assertEqual(
            self.combat_state.monsters_in_play[self.mock_player][0].name,
            "TestMonster"
        )

    def test_monster_faint(self):
        self.mock_monster.hp = 0
        self.assertEqual(self.mock_monster.hp, 0)
        self.combat_state.monsters_in_play[self.mock_player].append(self.mock_monster)
        self.combat_state.monsters_in_play[self.mock_player].remove(self.mock_monster)
        self.assertNotIn(self.mock_monster, self.combat_state.monsters_in_play[self.mock_player])

    def test_tuxemon_faints_during_battle(self):
        self.tuxemon.take_damage(15)
        self.assertEqual(self.tuxemon.current_hp, 0)
        self.assertTrue(self.tuxemon.is_fainted())
        self.battle.handle_fainted(self.tuxemon)
        self.assertNotIn(self.tuxemon, self.battle.active_tuxemon)
