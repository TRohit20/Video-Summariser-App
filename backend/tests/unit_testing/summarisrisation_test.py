import unittest
from backend.models.summariser import generate_summary

class SummarizationTests(unittest.TestCase):
    def test_generate_summary(self):
        transcript = 'Sample transcript'
        summary = generate_summary(transcript)
        self.assertTrue(isinstance(summary, str))

if __name__ == '__main__':
    unittest.main()
