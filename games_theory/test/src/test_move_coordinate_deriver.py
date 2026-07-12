import unittest

from games_theory.src.move_coordinate_deriver import MoveCoordinateDeriver


class MoveCoordinateDeriverTestCase(unittest.TestCase):
    def test_derives_top_left_coordinate(self):
        self.assertEqual(
            {'x': 0, 'y': 0},
            MoveCoordinateDeriver(2).derive("0,0,0,0", "-1,0,0,0"),
        )

    def test_derives_interior_coordinate(self):
        self.assertEqual(
            {'x': 1, 'y': 1},
            MoveCoordinateDeriver(3).derive(
                "0,0,0,0,0,0,0,0,0",
                "0,0,0,0,-1,0,0,0,0",
            ),
        )

    def test_rejects_transition_with_multiple_changed_cells(self):
        with self.assertRaisesRegex(ValueError, "exactly one cell"):
            MoveCoordinateDeriver(2).derive("0,0,0,0", "-1,-1,0,0")

    def test_rejects_transition_that_does_not_place_bot_marker(self):
        with self.assertRaisesRegex(ValueError, "bot marker"):
            MoveCoordinateDeriver(2).derive("0,0,0,0", "1,0,0,0")

    def test_rejects_state_with_wrong_cell_count(self):
        with self.assertRaisesRegex(ValueError, "board-size"):
            MoveCoordinateDeriver(2).derive("0,0,0", "-1,0,0")

    def test_rejects_non_positive_board_size(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            MoveCoordinateDeriver(0)


if __name__ == "__main__":
    unittest.main()
