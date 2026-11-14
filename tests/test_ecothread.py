"""Small, dependency-free regression tests for EcoThread's analysis."""

import unittest

from ecothread import analyze_source, calculate_co2_impact


class AnalyzeSourceTests(unittest.TestCase):
    def test_detects_nested_loops_through_control_flow(self):
        score, findings = analyze_source(
            "for item in items:\n    if item:\n        for other in items:\n            pass\n"
        )
        self.assertEqual(score, 90)
        self.assertEqual(len(findings), 1)
        self.assertIn("Line 1", findings[0])

    def test_no_nested_loops_has_full_heuristic_score(self):
        score, findings = analyze_source("for item in items:\n    print(item)\n")
        self.assertEqual((score, findings), (100, []))

    def test_score_is_bounded(self):
        source = "for a in x:\n" + "    for b in y:\n" * 12 + "        pass\n"
        score, _ = analyze_source(source)
        self.assertGreaterEqual(score, 0)


class CarbonEstimateTests(unittest.TestCase):
    def test_static_findings_do_not_claim_carbon_savings(self):
        self.assertIsNone(calculate_co2_impact(3))

    def test_computes_savings_from_explicit_inputs(self):
        # 100 W * 360 s = 0.01 kWh saved; at 400 g/kWh this is 4 g.
        self.assertEqual(
            calculate_co2_impact(
                1,
                before_seconds=600,
                after_seconds=240,
                power_w=100,
                grid_intensity_g_per_kwh=400,
            ),
            4.0,
        )

    def test_rejects_negative_measurements(self):
        with self.assertRaises(ValueError):
            calculate_co2_impact(
                before_seconds=1,
                after_seconds=0,
                power_w=-1,
                grid_intensity_g_per_kwh=400,
            )


if __name__ == "__main__":
    unittest.main()
