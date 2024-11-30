from dotenv import load_dotenv
import os


load_dotenv()  # take environment variables from .env.


VIRUS_API_KEY = os.environ.get('VIRUS_TOTAL_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
VERSION = '0.0.1'
PROJECT_NAME = 'usc'


USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
]

RESOLUTIONS = [
    '1920x1080',
]