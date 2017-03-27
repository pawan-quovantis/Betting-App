from server import app
from models import *
from resources import *
from routes import *

if __name__ == "__main__":
    app.run(debug=True)