import json
import unittest

from fresh_search import search

with open("examples/runbooks.json", encoding="utf-8") as fh:
    DOCS = json.load(fh)
Q = "how do I pause a delivery that is already sending"


class FreshSearchTest(unittest.TestCase):
    def test_plain_search_prefers_stale_runbook(self):
        self.assertEqual(search(DOCS, Q, fresh=False)[0][1], "RB-014")

    def test_fresh_search_drops_superseded(self):
        ids = [r[1] for r in search(DOCS, Q, fresh=True)]
        self.assertNotIn("RB-014", ids)
        self.assertEqual(ids[0], "RB-102")

    def test_past_review_flagged(self):
        notes = {r[1]: r[3] for r in search(DOCS, "quiet hours market", fresh=True)}
        self.assertIn("past review date", notes["RB-077"])


if __name__ == "__main__":
    unittest.main()
