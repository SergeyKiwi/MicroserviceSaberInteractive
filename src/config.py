import os

from dotenv import load_dotenv

load_dotenv()

IP = os.environ.get("IP")
PORT = int(os.environ.get("PORT"))
BUILDS_FILEPATH = os.environ.get("builds_filepath")
TASKS_FILEPATH = os.environ.get("tasks_filepath")