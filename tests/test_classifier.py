import unittest

from ai.classifier import classify_tone


class ClassifierTests(unittest.TestCase):
    def test_returns_unknown_for_empty_text(self) -> None:
        self.assertEqual(classify_tone("   "), "unknown")

    def test_formal_detection(self) -> None:
        self.assertEqual(classify_tone("Please review this request."), "formal")

    def test_informal_detection(self) -> None:
        self.assertEqual(classify_tone("hey bro this is gonna be awesome!"), "informal")

    def test_returns_unknown_when_no_formality_hints(self) -> None:
        self.assertEqual(classify_tone("This sentence has neutral wording"), "unknown")


if __name__ == "__main__":
    unittest.main()
