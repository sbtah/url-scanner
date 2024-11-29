from dotenv import load_dotenv
import os


load_dotenv()  # take environment variables from .env.


VIRUS_API_KEY = os.environ.get('VIRUS_TOTAL_API_KEY')


