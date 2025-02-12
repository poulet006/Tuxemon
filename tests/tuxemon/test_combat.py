# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2025 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
import unittest
from unittest import mock
from tuxemon.combat  import fainted
from tuxemon.monster import Monster

class TestCombat(unittest.TestCase):

    def setUp(self):
        self.tuxemon = Monster()
        self.opponent = Monster()

    def test_tuxemon_faints_during_combat(self):

        self.tuxemon.faint()

        self.assertEqual(self.tuxemon.current_hp, 0)

        self.assertTrue(self.tuxemon.hp == 0)

        #self.combat.fainted(self.tuxemon)

        #self.assertNotIn(self.tuxemon, self.combat.active_tuxemon)