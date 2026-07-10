import unittest

from games_theory.src.generator import Generator


class GeneratorTestCase(unittest.TestCase):
    def test_generate_neighbour_states(self):
        self.assertEqual(
            [
                "-1,1,0,0",
                "0,1,-1,0",
                "0,1,0,-1",
            ],
            Generator.generate_neighbour_states("0,1,0,0")
        )


if __name__ == "__main__":
    unittest.main()
