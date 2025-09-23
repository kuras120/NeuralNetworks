import unittest

from games_theory.helper.default_predictor import DefaultPredictor
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


class DefaultPredictorTestCase(unittest.TestCase):
    def test_generate_neighbour_states_returns_mutations_for_empty_cells(self):
        neighbours = DefaultPredictor._DefaultPredictor__generate_neighbour_states("NNON")
        expected_neighbours = [
            "ONON",
            "NOON",
            "NNOO",
        ]
        self.assertEqual(expected_neighbours, neighbours)

    def test_generate_neighbour_states_no_empty_cells(self):
        neighbours = DefaultPredictor._DefaultPredictor__generate_neighbour_states("OOOO")
        self.assertEqual([], neighbours)


if __name__ == '__main__':
    unittest.main()
