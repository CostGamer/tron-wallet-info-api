"""
Primary initialization, here we fill
necessary variables for the test environment
"""

from src.core import all_settings

# override for test
all_settings.database.host = "localhost"
all_settings.database.port = 5433
all_settings.database.user = "admin"
all_settings.database.password = "password"
all_settings.database.db_name = "postgres"
