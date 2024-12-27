from src.core import all_settings
from src.DB.db import get_session

get_session_instance = get_session(all_settings.database)
