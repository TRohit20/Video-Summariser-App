import unittest
from models.transcription import transcribe

class TranscriptionTests(unittest.TestCase):
    def test_transcribe(self):
        file_path = 'audio/sample.m4a'
        transcript = transcribe(file_path)
        self.assertTrue(isinstance(transcript, str))

if __name__ == '__main__':
    unittest.main()
