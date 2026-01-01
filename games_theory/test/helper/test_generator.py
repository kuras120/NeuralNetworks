import unittest

from games_theory.helper.generator import Generator


class GeneratorTestCase(unittest.TestCase):
    def test_generate_empty_state_populates_all_cells(self):
        q_table = {}
        state_hash = "NONNNONON"
        Generator.generate_empty_state(q_table, state_hash, length=3)

        expected_state = [
            [0, -1, 0],
            [0, 0, -1],
            [0, -1, 0],
        ]
        self.assertIn(state_hash, q_table)
        self.assertEqual(expected_state, q_table[state_hash])


if __name__ == "__main__":
    unittest.main()
