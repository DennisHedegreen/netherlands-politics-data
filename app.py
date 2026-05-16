import os

os.environ.setdefault("WPD_PROFILE", "netherlands_only")
os.environ.setdefault("WPD_APP_TITLE", "Dutch Politics Data")
os.environ.setdefault("WPD_EXPOSE_COUNTRIES", "netherlands")

from engine_app import main


main()
