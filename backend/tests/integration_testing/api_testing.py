import unittest
from unittest.mock import patch
from flask import Flask, current_app
from flask_testing import TestCase
from app import app

class APITests(TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_transcribe_route(self):
        response = self.client.post('/api/transcribe', data={
            'videoId': 'VIDEO_ID',
            'videoSource': 'youtube'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('transcription', data)
        self.assertIn('summary', data)

    def test_transcribe_route_invalid_source(self):
        response = self.client.post('/api/transcribe', data={
            'videoId': 'VIDEO_ID',
            'videoSource': 'invalid'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_transcribe_route_exception(self):
        with patch('whisper.load_model') as mock_load_model:
            mock_load_model.side_effect = Exception('Test exception')
            response = self.client.post('/api/transcribe', data={
                'videoId': 'VIDEO_ID',
                'videoSource': 'youtube'
            })
            data = response.get_json()
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
