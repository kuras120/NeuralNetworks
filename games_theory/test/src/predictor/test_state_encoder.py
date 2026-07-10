import unittest

from games_theory.src.predictor import StateEncoder


class StateEncoderTestCase(unittest.TestCase):
    def test_encode_cells_maps_board_relative_to_ai_playing_o(self):
        self.assertEqual(
            "1,-1,0,1",
            StateEncoder(ai_char='O').encode_cells(['X', 'O', 'N', 'X'])
        )

    def test_encode_cells_maps_board_relative_to_ai_playing_x(self):
        self.assertEqual(
            "-1,1,0,-1",
            StateEncoder(ai_char='X').encode_cells(['X', 'O', 'N', 'X'])
        )


if __name__ == "__main__":
    unittest.main()
