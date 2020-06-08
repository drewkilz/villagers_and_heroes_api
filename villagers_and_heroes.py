import os
from app import create_app
from configuration import ENV_FLASK_CONFIGURATION, DEVELOPMENT_KEY

app = create_app(os.getenv(ENV_FLASK_CONFIGURATION) or DEVELOPMENT_KEY)


if __name__ == '__main__':
    app.run()
