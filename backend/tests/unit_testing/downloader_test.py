import os
import unittest
from audio.downloader import download_youtube, download_vimeo

class DownloaderTests(unittest.TestCase):
    def test_download_youtube(self):
        video_id = 'VIDEO_ID'
        audio_path = download_youtube(video_id)
        self.assertTrue(os.path.isfile(audio_path))

    def test_download_vimeo(self):
        video_id = 'VIDEO_ID'
        audio_path = download_vimeo(video_id)
        self.assertTrue(os.path.isfile(audio_path))

if __name__ == '__main__':
    unittest.main()
