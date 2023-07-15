from unittest.mock import patch
from flask import app


def test_transcribe_route(self):
    with app.test_client() as client:
        response = client.post('/api/transcribe', data={
            'videoId': 'VIDEO_ID',
            'videoSource': 'youtube'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('transcription', data)
        self.assertIn('summary', data)

def test_transcribe_route_invalid_source(self):
    with app.test_client() as client:
        response = client.post('/api/transcribe', data={
            'videoId': 'VIDEO_ID',
            'videoSource': 'invalid'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

@patch('whisper.load_model')
def test_transcribe_route_exception(self, mock_load_model):
        mock_load_model.side_effect = Exception('Test exception')
        with app.test_client() as client:
            response = client.post('/api/transcribe', data={
                'videoId': 'VIDEO_ID',
                'videoSource': 'youtube'
            })
            data = response.get_json()
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', data)