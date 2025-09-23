import unittest

from games_theory.helper.default_predictor import DefaultPredictor


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


if __name__ == "__main__":
    unittest.main()
