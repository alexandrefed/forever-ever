import unittest
from compare_heals import compare, expected_useful


class HealingTests(unittest.TestCase):
    def setUp(self):
        self.spell = dict(name="synthetic", min_heal=100, max_heal=200,
                          mana=50, cast_seconds=0, gcd_seconds=1.5)

    def test_rolls_are_clipped_before_averaging(self):
        self.assertAlmostEqual(expected_useful(100, 200, 150), 137.5)

    def test_full_health_has_no_useful_healing(self):
        self.assertEqual(compare(self.spell, 0, 100)["useful_hp_per_mana"], 0)

    def test_instant_spell_is_still_gcd_limited(self):
        result = compare(self.spell, 500, 99)
        self.assertEqual(result["raw_hp_per_second"], 100)
        self.assertEqual(result["first_heal_seconds"], 0)
        self.assertEqual(result["casts_in_budget"], 1)

    def test_fixed_roll(self):
        self.assertEqual(expected_useful(100, 100, 1000), 100)

    def test_invalid_values(self):
        for key, value in [("mana", 0), ("min_heal", 201), ("cast_seconds", -1),
                           ("max_heal", float("nan")), ("mana", True)]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                compare({**self.spell, key: value}, 100, 100)


if __name__ == "__main__":
    unittest.main()
