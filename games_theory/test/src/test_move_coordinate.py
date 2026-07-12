import unittest

from games_theory.src.move_coordinate import derive_move_coordinate


class MoveCoordinateTestCase(unittest.TestCase):
    def test_derives_top_left_coordinate(self):
        self.assertEqual(
            {'x': 0, 'y': 0},
            derive_move_coordinate("0,0,0,0", "-1,0,0,0", 2),
        )

    def test_derives_interior_coordinate(self):
        self.assertEqual(
            {'x': 1, 'y': 1},
            derive_move_coordinate(
                "0,0,0,0,0,0,0,0,0",
                "0,0,0,0,-1,0,0,0,0",
                3,
            ),
        )

    def test_rejects_transition_with_multiple_changed_cells(self):
        with self.assertRaisesRegex(ValueError, "exactly one cell"):
            derive_move_coordinate("0,0,0,0", "-1,-1,0,0", 2)

    def test_rejects_transition_that_does_not_place_bot_marker(self):
        with self.assertRaisesRegex(ValueError, "bot marker"):
            derive_move_coordinate("0,0,0,0", "1,0,0,0", 2)

    def test_rejects_state_with_wrong_cell_count(self):
        with self.assertRaisesRegex(ValueError, "board-size"):
            derive_move_coordinate("0,0,0", "-1,0,0", 2)


if __name__ == "__main__":
    unittest.main()
