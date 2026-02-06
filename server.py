from os import getenv
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug_mode = getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=8000, debug=debug_mode)